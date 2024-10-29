import argparse
import logging

import pandas as pd

from core.dashboard.authorization_context import AuthorizationContext
from core.dashboard.resource_util import ResourceUtil


# pylint: disable=too-few-public-methods
class CSVGenerator:
    """Class that will change the csv to each case with a uid"""

    def __init__(self, auth_context):
        self.auth_context = auth_context

    def update_csv_with_uid(self, path_to_csv):
        logging.info("Reading active placements from dashboard API")

        resource_util = ResourceUtil(self.auth_context)
        csv_columns = ["name", "guid", "min_hour", "max_hour"]
        pl = resource_util.get_resource_index("/v2/manage/placements", "placement")
        pl_df = pd.DataFrame(pl, columns=["name", "guid"])
        pl_df_csv = pd.read_csv(
            path_to_csv,
            names=csv_columns,
            usecols=["name", "min_hour", "max_hour"],
        )
        pl_df_merged = pd.merge(pl_df_csv, pl_df, how="left", on="name")
        pl_df_merged.to_csv(
            path_to_csv,
            header=False,
            index=False,
            mode="w+",
            columns=csv_columns,
        )


logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(
    prog="csv_generator.py",
    description="This will update the csv with placements uid",
)
parser.add_argument(
    "--env",
    required=True,
    choices=["LOCAL", "DEV", "QA1", "QA2", "INT1"],
    help="The environment to update the csv",
)
parser.add_argument(
    "--dashboard_api",
    required=True,
    help="The url of the Dashboard API in the environment to update the csv",
)
parser.add_argument(
    "--dashboard_user",
    required=True,
    help="The dashboard user in the environment to update the csv",
)
parser.add_argument(
    "--dashboard_psw",
    required=True,
    help="The password of dashboard user in the environment to update the csv",
)
parser.add_argument(
    "--path_to_csv",
    required=True,
    help="The password of dashboard user in the environment to update the csv",
)

args = parser.parse_args()

CSVGenerator(
    AuthorizationContext(args.dashboard_api, args.dashboard_user, args.dashboard_psw)
).update_csv_with_uid(args.path_to_csv)
