import argparse
import json
import logging
import os

from core.dashboard.authorization_context import AuthorizationContext
from core.dashboard.resource_util import ResourceUtil
from core.data_exception import DataException

PATH_RESTRICTED_COMPANIES = "scripts/data/config/restricted_companies_ids.json"

PLACEMENT_URL = "/v2/manage/placements"


class PlacementCleanup:
    """This class is in charge of deleting all active placements to the company"""

    def __init__(self, environment, guid, context):
        self.environment = environment

        self.resource_util = ResourceUtil(context)
        self.guid = guid
        self.company_id = context.company_id

    def clean_up(self):
        """This method will delete all active placements using the Dashboard API"""

        self.validate_company_id_is_not_restricted()
        logging.info(
            "We are going to delete all active placements of the company with id [%s]",
            self.company_id,
        )
        placements = self.fetch_placements()
        deleted_placements = []
        for placement in placements:
            if (
                self.guid is None
                or len(self.guid) == 0
                or self.guid == placement.get("guid", "")
            ):
                self.delete_placement(placement)
                deleted_placements.append(placement)

        logging.info("Deleted [%s] placements", len(deleted_placements))

    def validate_company_id_is_not_restricted(self):
        """Make sure the company is not restricted"""
        if not os.path.isfile(PATH_RESTRICTED_COMPANIES):
            logging.error("the file restricted_companies_ids.json is not found")
            raise DataException("restricted_companies_ids.json is not found")

        with open(PATH_RESTRICTED_COMPANIES, "r", encoding="utf-8") as file:
            config_json_restricted_companies_ids = json.load(file)

        data_restricted_company_ids = config_json_restricted_companies_ids.get(
            self.environment, None
        )
        if data_restricted_company_ids is None:
            logging.error(
                "the file restricted_companies_ids.json does not contains data of environment %s",
                self.environment,
            )
            raise DataException(
                "the file restricted_companies_ids.json does not contains data of environment "
                + self.environment
            )
        for restricted_companies_id in data_restricted_company_ids:
            if int(self.company_id) == restricted_companies_id.get("companyId", 0):
                raise DataException(
                    "the company id "
                    + self.company_id
                    + " is restricted for env "
                    + self.environment
                    + " for the reason "
                    + restricted_companies_id.get("reason", "unknown")
                )

    def fetch_placements(self):
        return self.resource_util.get_resource_index(PLACEMENT_URL, "placement")

    def delete_placement(self, placement):
        resource_id = placement.get("id")
        resource_url = f"{PLACEMENT_URL}/{resource_id}"
        self.resource_util.delete_resource(resource_url, "placement")


def config_input_parameters():
    parser_input = argparse.ArgumentParser(
        prog="cleanup.py",
        description="A tool used to clean up all active placements in a company",
    )

    parser_input.add_argument(
        "--env",
        required=True,
        choices=["LOCAL", "DEV", "QA1", "QA2", "INT1"],
        help="The environment to be cleaned up",
    )
    parser_input.add_argument(
        "--dashboard_api",
        required=True,
        help="The url of the Dashboard API in the environment to be cleaned up",
    )
    parser_input.add_argument(
        "--dashboard_user",
        required=True,
        help="The dashboard user in the environment to be cleaned up",
    )
    parser_input.add_argument(
        "--dashboard_psw",
        required=True,
        help="The password of dashboard user in the environment to be cleaned up",
    )

    parser_input.add_argument(
        "--placement_guid",
        required=False,
        help="if this parameter is passed, only the specified placement is going to be deleted",
    )
    return parser_input


logging.basicConfig(level=logging.INFO)

parser = config_input_parameters()
args = parser.parse_args()

auth_context = AuthorizationContext(
    args.dashboard_api, args.dashboard_user, args.dashboard_psw
)
# will execute the cleanup
PlacementCleanup(args.env.upper(), args.placement_guid, auth_context).clean_up()
