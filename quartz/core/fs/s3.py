import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class S3:
    def __init__(self, bucket_name, sub_folder):
        self.bucket_name = bucket_name
        self.s3_resource = boto3.resource("s3")
        self.bucket = self.s3_resource.Bucket(bucket_name)
        self.sub_folder = sub_folder

    def delete_files(self, files_to_delete):
        for file_to_delete in files_to_delete:
            try:
                obj = self.bucket.Object(file_to_delete)
                obj.delete()
                obj.wait_until_not_exists()
                logger.info(
                    "Deleted object '%s' from bucket '%s'.",
                    file_to_delete,
                    self.bucket_name,
                )
            except ClientError:
                logger.exception(
                    "Couldn't delete object '%s' from bucket '%s'.",
                    file_to_delete,
                    self.bucket_name,
                )
                raise

    def write_data(self, data, filename):
        file_with_path = os.path.join(self.sub_folder, filename)
        try:
            obj = self.bucket.Object(file_with_path)
            obj.put(Body=data)
            obj.wait_until_exists()
            logger.info(
                "Put object '%s' to bucket '%s'.", file_with_path, self.bucket_name
            )
        except ClientError:
            logger.exception(
                "Couldn't put object '%s' to bucket '%s'.",
                file_with_path,
                self.bucket_name,
            )
            raise

    def close(self):
        pass

    def get_sub_folder(self):
        return self.sub_folder
