import logging

from context import Context
from resourceUtil import ResourceUtil, sanitize
from supplyDefaultValues import (
    PUBLISHER_DATA_DEFAULT,
    SITE_DATA_DEFAULT,
    DEFAULT_PLACEMENT_BODY,
)
from trackers import change_old_id_to_new_id_for_trackers

PLACEMENTS_PATH = "/v2/manage/placements"

SITES_PATH = "/v2/manage/sites"

PUBLISHERS_PATH = "/v2/manage/publishers"

PLACEMENTS_ALIGNMENTS_PATH = "/v2/manage/placements/alignments"


class Supply:
    def __init__(self, context: type(Context)):
        self.logger = logging.getLogger("upload")
        self.resource_util = ResourceUtil(context)
        self.api = context.configuration.dashboard_api

    def upload(self, resources, supply, trackers):
        supply_resources = resources.get("supply")
        publisher = self.__upload_publisher(supply_resources, supply.get("publisher"))
        site = self.__upload_site(supply_resources, publisher, supply.get("site"))
        placement = self.__upload_placement(
            supply_resources, site, supply.get("placement"), trackers
        )
        return {"publisher": publisher, "site": site, "placement": placement}

    def __upload_publisher(self, resources, publisher):
        url = self.api + PUBLISHERS_PATH
        publisher_request = sanitize(
            publisher, ["sites", "contactName", "contactEmail"]
        )

        publishers_by_name = resources.get("publishers")

        return self.resource_util.sync(
            url,
            publisher_request,
            publishers_by_name,
            PUBLISHER_DATA_DEFAULT,
            "publisher",
        )

    def __upload_site(self, resources, publisher, site):
        url = self.api + SITES_PATH
        site_tmp = sanitize(site, ["placements", "publisherName", "publisherId"])

        site_request = {"publisherId": publisher.get("id")}
        site_request.update(site_tmp)

        sites_by_name = resources.get("sites")

        return self.resource_util.sync(
            url,
            site_request,
            sites_by_name,
            SITE_DATA_DEFAULT,
            "site",
        )

    def __upload_placement(self, resources, site, placement, trackers):
        url = self.api + PLACEMENTS_PATH
        placement_tmp = sanitize(
            placement,
            ["publisherName", "siteId", "publisherId"],
        )
        old_trackers_id = placement_tmp.get("trackers")
        new_trackers_id = change_old_id_to_new_id_for_trackers(
            old_trackers_id, trackers
        )

        placement_request = {"siteId": site.get("id")}
        placement_request.update(placement_tmp)
        placement_request["trackers"] = new_trackers_id

        placements_by_name = resources.get("placements")

        return self.resource_util.sync(
            url,
            placement_request,
            placements_by_name,
            DEFAULT_PLACEMENT_BODY,
            "placement",
        )
