import csv
import gzip
import os
import uuid

from core.configuration import Configuration
from core.quartz import Quartz
from core.s3 import S3
from core.s3local import S3Local


class FileToUpload:
    def __init__(self, data_folder_path, original_file_name, generated_name):
        self.folder_path = data_folder_path
        self.original_file_name = original_file_name
        self.generated_name = generated_name

    def original_file_path(self):
        return f"{self.folder_path}/{self.original_file_name}"


class Uploader:
    def __init__(
        self,
        file: FileToUpload,
        external_config,
        fs,
        quartz,
        job_name,
        logger,
        processed_folder,
    ):
        self.file = file
        self.external_config = external_config
        self.fs = fs
        self.quartz = quartz
        self.job_name = job_name
        self.logger = logger
        self.processed_folder = processed_folder

    def execute(self):
        try:
            self.logger.info(f"Starting to process {self.file.original_file_name}")
            data = self.read()
            self.upload(data)
            self.run_quartz_job()
            self.check_success_of_file()
            self.logger.info(f"Finish to process {self.file.original_file_name}")
        finally:
            self.clean_up()

    def upload(self, data):
        self.fs.write_data(data, self.file.generated_name)

        return self

    def read(self):
        self.logger.info(f"Reading file [{self.file.original_file_name}]")
        return self

    def run_quartz_job(self):
        self.logger.info(f"Running the quartz job [{self.job_name}]")
        self.quartz.run_job(self.job_name)
        return self

    def check_success_of_file(self):
        file_name = self.file.generated_name
        self.logger.info(f"Searching the file {file_name} in the success folder")
        success_directory = os.path.join(self.processed_folder, "success")
        if not self.fs.is_file_found_in_folder(success_directory, file_name):
            self.logger.error(f"File {file_name} not found in success folder")
            raise Exception(f"File {file_name} doesn't exist in success folder")

        self.logger.info(f"The file {file_name} was found in success folder")

        return self

    def clean_up(self):
        file_name = self.file.generated_name
        self.logger.info(f"clean up of file {file_name}")
        base_name = os.path.splitext(file_name)[0]
        files_to_delete = [
            os.path.join(self.fs.get_sub_folder(), file_name),
            os.path.join(self.processed_folder, "success", file_name),
            os.path.join(self.processed_folder, "failed", file_name),
            os.path.join(self.processed_folder, "failed", base_name + ".failure"),
        ]
        self.fs.delete_files(files_to_delete)


class UploaderSegments(Uploader):
    def read(self):
        super().read()

        file_data = ""
        records_counter = 0
        with open(self.file.original_file_path()) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for line in tsv_file:
                if len(line) >= 2:
                    records_counter += 1
                    file_data += line[0] + "\t" + line[1] + "\n"

        self.logger.info(
            f"In the file [{self.file.original_file_name}] we have # of record of[{records_counter}]"
        )

        self.logger.debug(
            f"The content of the file [{self.file.original_file_name}] is \n[{file_data}]"
        )
        return gzip.compress(bytes(file_data, "utf-8"))


class UploaderTaxonomy(Uploader):
    def read(self):
        super().read()

        file_data = ""
        records_counter = 0
        with open(self.file.original_file_path()) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for line in tsv_file:
                if len(line) > 0:
                    records_counter += 1
                    file_data += (
                        "	".join(map(lambda x: f"{line[x]}", range(0, 10))) + "\n"
                    )

        self.logger.info(
            f"In the file [{self.file.original_file_name}] we have # of record of[{records_counter}]"
        )

        self.logger.debug(
            f"The content of the file [{self.file.original_file_name}] is \n[{file_data}]"
        )
        return file_data


class LiverampDataSyncJob:
    """This Class represent the adding/updating liveramp data by reading file from S3 an updating aerospike"""

    def __init__(
        self, root_path, build_number, log, external_config: Configuration = None
    ):

        self.external_config = external_config
        self.folder_audience_path = root_path + "/data/audience_data_files"
        self.quartz = Quartz(os.environ.get("DFQ_SERVER_ROOT_URL_DEFAULT"), log)
        self.build_number = build_number
        self.fs = self.load_strategy_uploader()
        self.logger = log

        self.logger.info(f"Starting to process liveramp")

    @staticmethod
    def load_strategy_uploader():
        bucket_name = os.getenv("S3_LIVERAMP_BUCKET_NAME")
        fs_sub_folder = os.getenv("LIVERAMP_BUCKET_SUB_FOLDER")
        local_liveramp_folder = os.environ.get("LOCAL_LIVERAMP_FOLDER", "")
        if len(local_liveramp_folder) > 0:
            return S3Local(local_liveramp_folder, fs_sub_folder)

        return S3(bucket_name, fs_sub_folder)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.fs.close()

    def execute(self):
        third_party_processed_folder = os.environ.get(
            "QRT_AUDIENCE_SEGMENT_3RD_PARTY_PROCESSED_SUB_FOLDER",
            "third_party_processed",
        )
        segments = [
            "lr_device_segments_automation_part000",
            "lr_web_segments_automation_part000",
        ]
        for segment_file in segments:
            UploaderSegments(
                FileToUpload(
                    self.folder_audience_path,
                    segment_file,
                    f"{segment_file}{self.build_number}uuid{uuid.uuid4()}.gz",
                ),
                self.external_config,
                self.fs,
                self.quartz,
                "liveramp.AudienceSegment3rdPartyJob",
                self.logger,
                third_party_processed_folder,
            ).execute()

        taxonomy_processed_folder = os.environ.get(
            "QRT_AUDIENCE_SEGMENT_TAXONOMY_PROCESSED_SUB_FOLDER",
            "taxonomy_processed",
        )
        UploaderTaxonomy(
            FileToUpload(
                self.folder_audience_path,
                "lr_ds_taxonomy_automationtest.tsv",
                f"lr_ds_taxonomy_automationtest{self.build_number}uuid{uuid.uuid4()}.tsv",
            ),
            self.external_config,
            self.fs,
            self.quartz,
            "liveramp.AudienceSegmentTaxonomyJob",
            self.logger,
            taxonomy_processed_folder,
        ).execute()
