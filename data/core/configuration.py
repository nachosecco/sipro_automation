import logging
import os

from core.util.app_utils import check_and_get_env


class Configuration:
    """Class to get configuration parameters from environmental variables"""

    def __init__(self):
        self.csv_path_file = os.getenv("DPR_PATH_CSV")
        self.execution_id = os.getenv("DPR_EXECUTION_ID")
        self.path_case_events = check_and_get_env("DPR_PATH_CASE_EVENTS")
        self.athena_database = check_and_get_env("DSE_ENVIRONMENT").lower()

    @staticmethod
    def get_delivery_url():
        root_url_delivery = "DELIVERY_ROOT_URL"

        if root_url_delivery in os.environ:
            logging.info(
                f"{root_url_delivery} value is {os.environ[root_url_delivery]}"
            )

        else:
            logging.error(
                f"{root_url_delivery} does not exist, please set the environmental variable DELIVERY_ROOT_URL"
            )
            raise ValueError(
                "the environmental variable DELIVERY_ROOT_URL is undefined"
            )

        return os.environ[root_url_delivery]
