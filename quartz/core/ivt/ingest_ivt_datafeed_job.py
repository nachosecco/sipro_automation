import logging as log
import os
import uuid
from abc import abstractmethod

import redis
from core.fs.local import Local
from core.fs.sftp import SFTP
from core.quartz import Quartz


class IngestIVTDataFeedJob:
    def __init__(self, fs_sub_folder):
        # properties to be set by the child
        self.job_name = ""
        self.source_filename_prefix = ""
        self.redis_key_prefix = ""
        self.file_key_col_name = ""

        self.data_files = []
        self.quartz = Quartz()

        local_source_folder = os.environ.get("QRT_IVT_LOCAL_FOLDER")
        if local_source_folder:
            log.info("Running on local")
            self.fs = Local(local_source_folder, fs_sub_folder)
        else:
            self.fs = SFTP(fs_sub_folder)

        self.redis_host = os.environ.get("QRT_REDIS_HOST", "localhost")
        self.redis_port = int(os.environ.get("QRT_REDIS_PORT", 6379))
        self.redis_client = redis.Redis(
            host=self.redis_host, port=self.redis_port, db=0
        )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.__clean_fs()
        self.__clean_redis()
        self.fs.close()
        self.redis_client.close()

    def add_file(self, records):
        self.__add_data_file(f"{self.source_filename_prefix}", records)

    def get_record_by_key(self, key):
        return self.redis_client.get(self.redis_key_prefix + key)

    def execute(self, skip_redis_clean=False):
        if not skip_redis_clean:
            self.__clean_redis()

        self.upload_data_to_fs()
        self.quartz.run_job(self.job_name)

    def __add_data_file(self, filename, records):
        filename += str(uuid.uuid4()) + ".csv"

        self.data_files.append({"filename": filename, "records": records})

    def __clean_fs(self):
        for file in self.data_files:
            file_name = os.path.join(self.fs.get_sub_folder(), file["filename"])
            base_name = os.path.splitext(file_name)[0]
            files_to_delete = [
                file_name,
                base_name + ".success",
                base_name + ".failure",
            ]
            self.fs.delete_files(files_to_delete)

    def __clean_redis(self):
        for file in self.data_files:
            for record in file["records"]:
                try:
                    self.redis_client.delete(
                        self.redis_key_prefix + record[self.file_key_col_name]
                    )
                except redis.exceptions.DataError:
                    pass

    @abstractmethod
    def upload_data_to_fs(self):
        raise NotImplementedError()
