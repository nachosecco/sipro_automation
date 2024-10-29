import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class S3:
    """This class represent the AWS S3 Operations like reading, writing and deleting the files"""

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_resource = boto3.resource("s3")
        self.bucket = self.s3_resource.Bucket(bucket_name)

    def delete_folder(self, folder_name):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.bucket_name)
        try:
            logging.info("Attempting to delete folder %s", folder_name)
            # List all objects in the folder
            objects_to_delete = bucket.objects.filter(Prefix=folder_name)

            # Delete all objects in the folder
            for obj in objects_to_delete:
                obj.delete()
                print(f"Deleted {obj.key}")

        except ClientError as e:
            print(f"Error: {e}")

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
