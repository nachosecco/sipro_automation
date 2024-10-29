import gzip
import os
import uuid

import aerospike
from aerospike import exception as aero_ex
from core.fs.local import Local
from core.fs.s3 import S3
from core.quartz import Quartz


class AudienceSegment3rdPartyJob:
    def __init__(self):
        self.job_name = "liveramp.AudienceSegment3rdPartyJob"
        self.data_files = []

        self.quartz = Quartz()

        local_liveramp_folder = os.environ.get("QRT_LOCAL_LIVERAMP_FOLDER")
        bucket_name = os.environ.get(
            "QRT_S3_LIVERAMP_BUCKET_NAME", "c6-dev-s3-uw2-liveramp"
        )
        self.fs_sub_folder = os.environ.get(
            "QRT_AUDIENCE_SEGMENT_3RD_PARTY_SUB_FOLDER", "upload"
        )

        self.fs_processed_folder = os.environ.get(
            "QRT_AUDIENCE_SEGMENT_3RD_PARTY_PROCESSED_SUB_FOLDER",
            "third_party_processed",
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
        self.aero_segment_bin = "segments"

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.__clean_fs()
        self.__clean_aerospike()
        self.fs.close()
        self.aero_client.close()

    def add_lr_device_file(self, devices):
        self.__add_data_file("lr_device_segments_regression_test_", devices)

    def add_lr_cookie_file(self, devices):
        self.__add_data_file("lr_web_segments_regression_test_", devices)

    def execute(self, skip_aerospike_clean=False):
        if not skip_aerospike_clean:
            self.__clean_aerospike()

        self.__upload_data_to_fs()
        self.quartz.run_job(self.job_name)

    def get_lr_device_segments_as_list(self, device_id):
        aero_key = (self.aero_namespace, self.aero_set, device_id)
        return self.__get_segments_as_list(aero_key, self.aero_segment_bin)

    def get_lr_cookie_segments_as_list(self, cookie_id):
        aero_key = (self.aero_namespace, self.aero_set, cookie_id)
        return self.__get_segments_as_list(aero_key, self.aero_segment_bin)

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
