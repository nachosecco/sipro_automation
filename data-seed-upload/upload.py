#!python
import argparse
import logging
import os
import traceback

from uploadDashboardApi import UploadDashboardApi
from uploadInventoryRouters import UploadInventoryRouters

JSON_FILES_TO_IGNORE_FOR_DELIVERY = ["test_get_inventory_routers_ok.json"]

parser = argparse.ArgumentParser(
    prog="upload.py",
    description="A tool used to upload data serialized by data-seed-extractor",
)
parser.add_argument(
    "app_to_upload",
    choices=["delivery", "inventory_routers"],
    help="Which app type we are uploading",
)
parser.add_argument("path", help="Path to file or folder to be uploaded")
parser.add_argument(
    "--upload-all",
    action="store_true",
    help="Upload all data even if the placement already exists",
)

args = parser.parse_args()
print(f"Parsed Arguments are: ${vars(args)}")

path = args.path

if not (os.path.exists(path)):
    raise Exception(f"The {path} does not exists")


def upload(api_object):
    logger = logging.getLogger("upload")
    if os.path.isfile(path):
        logger.info(f"Uploading a single file {path}")
        api_object.upload_file(path)
    else:
        logger.info(f"Uploading a folder {path}")
        files_to_upload = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".json") and (
                    args.app_to_upload == "delivery"
                    and file not in JSON_FILES_TO_IGNORE_FOR_DELIVERY
                ):
                    files_to_upload.append(os.path.join(root, file))
        number_of_files_uploaded = 0
        total_number_of_files_to_upload = len(files_to_upload)
        files_with_problems = []
        for file in files_to_upload:
            number_of_files_uploaded += 1

            try:
                logger.info(
                    f"\nUploading {number_of_files_uploaded}/{total_number_of_files_to_upload}."
                    f" \n File in progress is {file}"
                )
                api_object.upload_file(file)

            except Exception as e:
                traceback.print_exc()
                logger.error(f"Error {e} processing {file}")
                files_with_problems.append(file)
        processed = len(files_to_upload) - len(files_with_problems)
        logger.info(f"It was Processed {processed}/{len(files_to_upload)}")

        if len(files_with_problems) > 0:
            logger.warning(
                f"There was {len(files_with_problems)} error processing {files_with_problems}"
            )


if args.app_to_upload == "delivery":
    print("About to launch upload information for delivery")
    only_new_changes = not args.upload_all
    upload(UploadDashboardApi(only_new_changes))

if args.app_to_upload == "inventory_routers":
    print("About to launch upload information for inventory routers")
    upload(UploadInventoryRouters())
