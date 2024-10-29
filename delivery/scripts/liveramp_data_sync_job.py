import logging
import os.path
import sys

from core.liveramp_data_sync_job import LiverampDataSyncJob


def setup_logger():
    logging.basicConfig(format="%(asctime)s [%(levelname)8.8s] %(message)s")

    logger = logging.getLogger("csv")
    logger.setLevel(logging.DEBUG)
    return logger


# This script will be executed for adding/updating liveramp data from device & web segment and taxonomy file. This
# data will be further used in cases
def liveramp_data_sync_job():
    if len(sys.argv) == 1:
        root_path = os.path.abspath("..")
        build_number = ""
    else:
        root_path = sys.argv[1]
        build_number = f"J{sys.argv[2]}"
    LiverampDataSyncJob(root_path, build_number, setup_logger()).execute()


liveramp_data_sync_job()
