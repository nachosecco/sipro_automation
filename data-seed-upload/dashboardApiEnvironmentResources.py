import logging

from context import Context
from demand import (
    ADVERTISERS,
    INSERTION_ORDERS,
    CAMPAIGNS,
    MEDIA,
    AUDIENCES,
)
from programmaticDemand import PROGRAMMATIC_DEMAND, RTB_BIDDERS
from resourceUtil import ResourceUtil
from supply import (
    PUBLISHERS_PATH,
    SITES_PATH,
    PLACEMENTS_PATH,
    PLACEMENTS_ALIGNMENTS_PATH,
)
from trackers import TRACKERS

PREFIX_REGRESSION_CASE_NAME = "test_"
COMPANIES_PATH = "/v2/manage/companies"


def to_name_value(resources, resource_name_log, filter_by_name=True, name_key="name"):
    """It will convert from array to key/value where the key is going to be the name
    and filter the collection with name a PREFIX"""

    index_resources = {}

    for resource in resources:
        name = resource.get(name_key)
        if (filter_by_name and name.startswith(PREFIX_REGRESSION_CASE_NAME)) or not (
            filter_by_name
        ):
            existing_value = index_resources.get(name, None)
            if existing_value is not None:
                existing_id = existing_value.get("id")
                new_id = resource.get("id")
                logging.warning(
                    f"We have a duplicated resource {name_key} [{name}] with id [{existing_id}] is going "
                    f"and is going to be replace with other id [{new_id}] for resource of [{resource_name_log}]"
                )

            index_resources[name] = resource
    return index_resources


def to_key_value(resources, resource_name_log, key):
    """It will convert from array to key/value where the key is going to be the `key`"""

    index_resources = {}

    for resource in resources:
        key_value = resource.get(key)

        existing_value = index_resources.get(key_value, None)
        if existing_value is not None:
            logging.warning(
                f"We have a duplicated resource in key {key} with the value [{existing_value}]"
                f" for resource of [{resource_name_log}]"
            )

        index_resources[key_value] = resource
    return index_resources


class DashboardApiEnvironmentResources:
    def __init__(
        self,
    ):
        self.logger = logging.getLogger("upload")

    def load_companies(self, context: type(Context)):
        self.logger.info("Loading companies")
        resource_util = ResourceUtil(context)
        url = f"{context.configuration.dashboard_api}{COMPANIES_PATH}"
        return to_name_value(
            resource_util.load_index(url, "companies"),
            "companies",
            filter_by_name=False,
        )

    def load_resources(self, context: type(Context)):
        self.logger.info("Loading resources")
        resource_util = ResourceUtil(context)
        # Alias to the method
        resources = resource_util.load_index
        api = context.configuration.dashboard_api
        self.logger.info("Loading resources supply")
        # Supply
        publishers = to_name_value(
            resources(f"{api}{PUBLISHERS_PATH}", "publisher"), "publisher"
        )
        sites = to_name_value(resources(f"{api}{SITES_PATH}", "site"), "site")
        placements = to_name_value(
            resources(f"{api}{PLACEMENTS_PATH}", "placement"), "placement"
        )
        # Demand Sources
        self.logger.info("Loading resources demand sources")
        advertisers = to_name_value(
            resources(f"{api}{ADVERTISERS}", "advertiser"), "advertiser"
        )
        insertion_orders = to_name_value(
            resources(f"{api}{INSERTION_ORDERS}", "insertion-order"), "insertion-order"
        )
        campaigns = to_name_value(
            resources(f"{api}{CAMPAIGNS}", "campaign"), "campaign"
        )
        media = to_name_value(resources(f"{api}{MEDIA}", "media"), "media")

        self.logger.info("Loading resources rtb")
        # We are reading the seat information from the environment,
        # seat information is part of the programmatic demand, and we can reuse later doing
        # the upload for programmatic demand
        programmatic_demands = to_name_value(
            resources(f"{api}{PROGRAMMATIC_DEMAND}", "programmatic-demand"), False
        )
        deals_programmatic_demands = {}
        for programmatic_demand in programmatic_demands.values():
            deal_id = programmatic_demand.get("dealId", None)
            if deal_id is not None and len(deal_id) > 0:
                deals_programmatic_demands[deal_id] = programmatic_demand

        rtb_bidders = to_name_value(
            resources(f"{api}{RTB_BIDDERS}", "rtb-bidder"), "rtb-bidder"
        )

        audiences = to_name_value(
            resources(f"{api}{AUDIENCES}", "audiences"),
            "audiences",
            True,
            "description",
        )

        self.logger.info("Loading resources trackers")

        resources_trackers = resources(f"{api}{TRACKERS}", "tracker")
        trackers_by_name = to_name_value(resources_trackers, "trackers", False)
        trackers_by_url_type = {}
        for tracker in trackers_by_name.values():
            tracker_url = tracker.get("url")
            tracker_type = tracker.get("type")
            trackers_by_url_type[f"{tracker_url}{tracker_type}"] = tracker

        alignments = to_key_value(
            resources(f"{api}{PLACEMENTS_ALIGNMENTS_PATH}", "alignments"),
            "alignments",
            "idPlacement",
        )

        return {
            "supply": {
                "publishers": publishers,
                "sites": sites,
                "placements": placements,
            },
            "demand": {
                "advertisers": advertisers,
                "insertion-orders": insertion_orders,
                "campaigns": campaigns,
                "media": media,
                "programmatic_demands": programmatic_demands,
                "deals": deals_programmatic_demands,
                "rtb_bidders": rtb_bidders,
                "audiences": audiences,
            },
            "trackers": {"name": trackers_by_name, "url_type": trackers_by_url_type},
            "alignments": alignments,
        }
