import gzip
import os
import uuid

import aerospike
from aerospike import exception as aero_ex
from core.domain import Domain
from core.fs.local import Local
from core.fs.s3 import S3
from core.quartz import Quartz


def get_segment_filename(segment_filename_prefix):
    return f"{segment_filename_prefix}_device_segments_regression_test_"


DEFAULT_AERO_SEGMENT_BIN = "regression-dds"


class AudienceSegment1stPartyJob:
    def __init__(self):
        self.job_name = "liveramp.AudienceSegment1stPartyJob"
        self.segment_filename_prefix = "regression_1st_party"
        self.data_files = []
        self.additional_data_distributions = []

        self.domain = Domain()
        self.quartz = Quartz()

        local_liveramp_folder = os.environ.get("QRT_LOCAL_LIVERAMP_FOLDER")
        bucket_name = os.environ.get(
            "QRT_S3_LIVERAMP_BUCKET_NAME", "c6-dev-s3-uw2-liveramp"
        )
        self.fs_sub_folder = os.environ.get(
            "QRT_AUDIENCE_SEGMENT_1ST_PARTY_SUB_FOLDER", "first_party"
        )
        self.fs_processed_folder = os.environ.get(
            "QRT_AUDIENCE_SEGMENT_1ST_PARTY_PROCESSED_SUB_FOLDER",
            "first_party_processed",
        )

        if local_liveramp_folder:
            self.fs = Local(local_liveramp_folder, self.fs_sub_folder)
        else:
            self.fs = S3(bucket_name, self.fs_sub_folder)

        self.aerospike_host = os.environ.get("QRT_AEROSPIKE_HOST", "localhost")
        self.aerospike_port = int(os.environ.get("QRT_AEROSPIKE_PORT", 3000))
        self.aero_config = {"hosts": [(self.aerospike_host, self.aerospike_port)]}
        self.aero_client = aerospike.client(self.aero_config).connect()
        self.aero_namespace = "tempcache"
        self.aero_set = "audience_targeting_segments"
        self.aero_segment_bin = DEFAULT_AERO_SEGMENT_BIN

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.__clean_db()
        self.__clean_fs()
        self.__clean_aerospike()
        self.fs.close()
        self.aero_client.close()

    def add_1st_party_device_file(self, devices):
        self.__add_data_file(
            get_segment_filename(self.segment_filename_prefix), devices
        )

    def add_1st_party_device_file_with_prefix(self, devices, segment_filename_prefix):
        self.__add_data_file(get_segment_filename(segment_filename_prefix), devices)

    def add_1st_party_cookie_file(self, devices):
        self.__add_data_file(
            f"{self.segment_filename_prefix}_web_segments_regression_test_", devices
        )

    def set_additional_data_distributions(self, additional_data_distributions):
        self.additional_data_distributions = additional_data_distributions

    def execute(self, skip_aerospike_clean=False):
        if not skip_aerospike_clean:
            self.__clean_aerospike()

        self.__prepare_db()
        self.__upload_data_to_fs()
        self.quartz.run_job(self.job_name)

    def get_1st_party_device_segments_as_list(self, device_id):
        aero_key = (self.aero_namespace, self.aero_set, device_id)
        return self.__get_segments_as_list(aero_key, self.aero_segment_bin)

    def get_1st_party_cookie_segments_as_list(self, cookie_id):
        aero_key = (self.aero_namespace, self.aero_set, cookie_id)
        return self.__get_segments_as_list(aero_key, self.aero_segment_bin)

    def get_bins_for_device_id(self, device_id):
        aero_key = (self.aero_namespace, self.aero_set, device_id)
        (key_, meta, bins) = self.aero_client.get(aero_key)
        return bins

    def __get_segments_as_list(self, aero_key, bin_name):
        (key_, meta, bins) = self.aero_client.get(aero_key)

        if bin_name not in bins:
            raise Exception(f"bin name {bin_name} not present for key {aero_key}")

        return bins[bin_name]

    def __add_data_file(self, filename, devices):
        filename += str(uuid.uuid4()) + ".gz"

        self.data_files.append({"filename": filename, "devices": devices})

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

    def __clean_aerospike(self):
        for file in self.data_files:
            for device in file["devices"]:
                aero_key = (self.aero_namespace, self.aero_set, device["id"])
                try:
                    self.aero_client.remove(aero_key)
                except aero_ex.RecordNotFound:
                    pass

    def __upload_data_to_fs(self):
        for file in self.data_files:
            file_data = ""
            for device in file["devices"]:
                file_data += device["id"] + "\t" + ",".join(device["segments"]) + "\n"

            self.fs.write_data(
                gzip.compress(bytes(file_data, "utf-8")), file["filename"]
            )

    def insert_into_data_distribution(
        self,
        default_name,
        display_name,
        status,
        aerospike_bin_name,
        segment_filename_prefix,
    ):
        sql = f"""
        INSERT INTO data_distribution (
            default_name, display_name, status,
            aerospike_bin_name, segment_filename_prefix, created_at, updated_at)
        VALUES (
            '{default_name}', '{display_name}', '{status}',
            '{aerospike_bin_name}', '{segment_filename_prefix}', now(), now());
        """
        self.domain.execute(sql)

    def __prepare_db(self):
        self.__clean_db()
        # Our main data distribution
        self.insert_into_data_distribution(
            "Regression_Testing_1st_Party_DDS",
            "Regression Testing 1st Party Data Store",
            "active",
            self.aero_segment_bin,
            self.segment_filename_prefix,
        )
        # Additional data distributions
        for data_distribution in self.additional_data_distributions:
            self.insert_into_data_distribution(
                data_distribution["default_name"],
                data_distribution["display_name"],
                data_distribution["status"],
                data_distribution["aerospike_bin_name"],
                data_distribution["segment_filename_prefix"],
            )

    def __clean_db(self):
        segment_filename_prefixes = [
            data_distribution["segment_filename_prefix"]
            for data_distribution in self.additional_data_distributions
        ]
        segment_filename_prefixes.append(self.segment_filename_prefix)
        sql = f"""
        DELETE FROM data_distribution
        WHERE segment_filename_prefix IN ('{"','".join(segment_filename_prefixes)}');
        """
        self.domain.execute(sql)
