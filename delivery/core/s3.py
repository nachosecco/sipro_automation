import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class S3:
    """This class represent the AWS S3 Operations like reading, writing and deleting the files"""

    def __init__(self, bucket_name, sub_folder):
        self.bucket_name = bucket_name
        self.s3_resource = boto3.resource("s3")
        self.bucket = self.s3_resource.Bucket(bucket_name)
        self.sub_folder = sub_folder

    def is_file_found_in_folder(self, folder, expected_file_name):
        for obj in self.s3_resource.Bucket(name=self.bucket_name).objects.filter(
            Prefix=folder
        ):
            filename = obj.key.split("/")[-1]
            if filename == expected_file_name:
                return bool(True)

    def delete_files(self, files):
        for file_to_delete in files:
            try:
                obj = self.bucket.Object(file_to_delete)
                obj.delete()
                obj.wait_until_not_exists()
                logger.info(
                    "Deleted object '%s' from bucket '%s'.",
                    file_to_delete,
                    self.bucket_name,
                )
            except ClientError as ce:
                logger.exception(
                    "Couldn't delete object '%s' from bucket '%s'. The Error "
                    + str(ce),
                    file_to_delete,
                    self.bucket_name,
                )
                raise

    def write_data(self, data, remote_filename):
        remote_file = os.path.join(self.sub_folder, remote_filename)
        try:
            obj = self.bucket.Object(remote_file)
            obj.put(Body=data)
            obj.wait_until_exists()
            logger.info(
                "Put object '%s' to bucket '%s'.", remote_file, self.bucket_name
            )
        except ClientError as ce:
            logger.exception(
                "Couldn't put object '%s' to bucket '%s'. The error " + str(ce),
                remote_file,
                self.bucket_name,
            )
            raise

    def close(self):
        logger.info("Nothing to do")

    def get_sub_folder(self):
        return self.sub_folder
