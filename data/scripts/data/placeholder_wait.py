import argparse
import logging
import sys
from datetime import datetime
from time import sleep

from core.case import Case
from core.configuration import Configuration
from core.data_exception import DataException
from core.query import druid
from core.query.druid_config import DruidConfig
from core.util.app_utils import check_and_get_env


# pylint: disable=too-few-public-methods
class PlaceholderWait:
    """Class that Queries Druid every minute to check if the placeholder data is in druid"""

    def __init__(self, timeout_wait):
        self.druid_config = DruidConfig()
        self.timeout_wait = int(timeout_wait)

    def wait(self, timeout):
        start_time = datetime.now()
        configuration = Configuration()
        configuration.csv_path_file = check_and_get_env("DPR_PATH_PLACEHOLDER_CSV")

        case = Case("test_placeholder", configuration)
        placement_uuid = case.delivery_parameters.uid
        logging.info("Placement UUID for test placeholder: %s", placement_uuid)

        timeout_in_hours = int(timeout / 3600) + 2
        druid_query = {
            "query": f"select count(*) from network_v1 WHERE __time >= CURRENT_TIMESTAMP - "
            f"INTERVAL '{timeout_in_hours}' HOUR and placement = '{placement_uuid}'",
            "resultFormat": "csv",
        }
        timer = 0
        while timer <= timeout:
            druid_query_results = druid.query(
                self.druid_config.druid_url,
                self.druid_config.druid_username,
                self.druid_config.druid_password,
                druid_query,
            )
            logging.info("Test placeholder impression count: %s", druid_query_results)
            if int(druid_query_results) > 0:
                logging.info("Found test placeholder events")
                return
            minutes_diff = (datetime.now() - start_time).total_seconds() / 60.0
            if minutes_diff > self.timeout_wait:
                raise DataException("timeout waiting for placeholder events")
            sleep(60)
        logging.error("Can't detect test placeholder event after %s seconds", timeout)
        sys.exit(1)


def config_input_parameters():
    parser_input = argparse.ArgumentParser(
        prog="placement_wait.py",
        description="Queries Druid every minute to check if the placeholder data is in druid",
    )

    parser_input.add_argument(
        "--timeout",
        required=False,
        help="if this parameter is set, the timeout will be changed from the default value of 3600 seconds",
        default="3600",
    )

    parser_input.add_argument(
        "--timeout_wait",
        required=True,
        help="is the max time in minutes to actually wait that the placeholder is found",
    )

    return parser_input


logging.basicConfig(level=logging.INFO)

parser = config_input_parameters()
args = parser.parse_args()

PlaceholderWait(args.timeout_wait).wait(int(args.timeout))
