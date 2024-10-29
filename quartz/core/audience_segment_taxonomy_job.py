import os
import uuid

from core.domain import Domain
from core.fs.local import Local
from core.fs.s3 import S3
from core.quartz import Quartz


class AudienceSegmentTaxonomyJob:
    def __init__(self):
        self.job_name = "liveramp.AudienceSegmentTaxonomyJob"
        self.data_files = []
        self.audiences = []

        self.domain = Domain()
        self.quartz = Quartz()

        local_liveramp_folder = os.environ.get("QRT_LOCAL_LIVERAMP_FOLDER")
        bucket_name = os.environ.get(
            "QRT_S3_LIVERAMP_BUCKET_NAME", "c6-dev-s3-uw2-liveramp"
        )
        self.fs_sub_folder = os.environ.get(
            "QRT_AUDIENCE_SEGMENT_TAXONOMY_SUB_FOLDER", "upload"
        )

        self.fs_processed_folder = os.environ.get(
            "QRT_AUDIENCE_SEGMENT_TAXONOMY_PROCESSED_SUB_FOLDER",
            "taxonomy_processed",
        )

        if local_liveramp_folder:
            self.fs = Local(local_liveramp_folder, self.fs_sub_folder)
        else:
            self.fs = S3(bucket_name, self.fs_sub_folder)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.__clean_fs()
        self.__clean_db()
        self.fs.close()

    def add_lr_taxonomy_file(self, content):
        self.__add_data_file("lr_ds_taxonomy_regression_test_", content)

    def execute(self, skip_db_clean=False):
        if not skip_db_clean:
            self.__clean_db()

        self.__upload_data_to_fs()
        self.quartz.run_job(self.job_name)

    def get_segment(self, segment_id):
        return self.domain.retrieve(
            "SELECT * FROM audience_segment where segment_id='%s'" % segment_id
        )

    def get_audience(self, audience_guid):
        return self.domain.retrieve(
            """SELECT * FROM audience where guid ='%s'""" % audience_guid
        )

    def add_audience(self, company_id, guid, expression):
        sql = """insert into audience (
           company_id, guid, name, description,
           max_cpm,min_cpm,
           potential_device_reach,
           potential_reach,status,expression)
        values (%s, %s,'TestAudience','An audience 4 test', 0, 0, 0, 0,'active',%s)"""
        self.audiences.append(guid)
        self.domain.execute(sql, (company_id, guid, expression))

    def __add_data_file(self, filename, content):
        filename += str(uuid.uuid4()) + ".csv"
        self.data_files.append({"filename": filename, "content": content})

    def __clean_fs(self):
        for file in self.data_files:
            file_name = file["filename"]
            base_name = os.path.splitext(file_name)[0]
            files_to_delete = [
                os.path.join(self.fs_sub_folder, file_name),
                os.path.join(self.fs_processed_folder, "success", file_name),
                os.path.join(self.fs_processed_folder, "failed", file_name),
                os.path.join(
                    self.fs_processed_folder, "failed", base_name + ".failure"
                ),
            ]
            self.fs.delete_files(files_to_delete)

    def __clean_db(self):
        for file in self.data_files:
            for content in file["content"]:
                self.domain.execute(
                    """DELETE FROM audience_segment WHERE segment_id = %s""",
                    (content["segment_id"],),
                )
        for audience in self.audiences:
            self.domain.execute("""DELETE FROM audience where guid=%s""", (audience,))

    def __upload_data_to_fs(self):
        file_header = (
            "Segment_ID\\tKey\\tValue\\tProvider Name\\tSegment Name\\t"
            "Segment Description\\tUse Restrictions\\tPermitted Advertisers\\t"
            "Custom\\tPrice ($CPM)\n"
        )

        file_line_format = (
            "%s\tB2B Audience > Currently Employed\t1\tCybba"
            "\tCybba > B2B Audience > Currently Employed"
            "\tUse this segment to target users currently employed in the United States."
            "\t\t\tfalse\t%f\n"
        )

        for file in self.data_files:
            file_data = file_header
            for content in file["content"]:
                file_data += file_line_format % (content["segment_id"], content["cpm"])
                self.fs.write_data(bytes(file_data, "utf-8"), file["filename"])
