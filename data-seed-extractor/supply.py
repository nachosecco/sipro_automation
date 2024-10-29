import logging

from context import Context
from resourceUtil import ResourceUtil


class Supply:
    def __init__(self, context: type(Context), context_placement):
        self.context = context
        self.context_placement = context_placement
        self.logger = logging.getLogger("extractor")
        self.resource_util = ResourceUtil(context.authorization_context)
        self.api = self.context.configuration.dashboard_api

    def extract(self):

        placement = self._load_placement()

        site = self.__load_site(placement)
        publisher = self.__load_publisher(site)

        trackers = self.__load_trackers(placement)

        return {
            "placement": placement,
            "site": site,
            "publisher": publisher,
            "trackers": trackers,
        }

    def _load_placement(self):

        # If we have the uid, then id should be there, and we are going to search the placement by id
        if self.context_placement.get("uid") is None:
            return self.__load_placement_by_id(self.context_placement.get("id"))

        placements = self.__load_index_placements()
        return self.__load_placement_by_index(placements)

    @staticmethod
    def __load_trackers(placement):
        trackers_to_return = set()
        trackers = placement.get("trackers")
        if trackers is not None:
            for tracker in trackers:
                trackers_to_return.add(tracker)

        return list(trackers_to_return)

    def __load_placement_by_index(self, placements):
        for placement in placements:
            if placement.get("guid") == self.context_placement.get("uid"):
                return self.__load_placement_by_id(placement.get("id"))

    def __load_index_placements(self):

        url = f"{self.api}/v2/manage/placements?siteId="

        return self.resource_util.get_resource_index("placement", url)

    def __load_site(self, placement):
        site_id = placement["siteId"]
        url = f"{self.api}/v2/manage/sites/{site_id}"

        return self.resource_util.get_resource_with_test_case_naming(
            site_id, "site", url, self.context.case_name
        )

    def __load_publisher(self, site):

        publisher_id = site["publisherId"]
        url = f"{self.api}/v2/manage/publishers/{publisher_id}"

        return self.resource_util.get_resource_with_test_case_naming(
            publisher_id, "publisher", url, self.context.case_name
        )

    def __load_placement_by_id(self, placement_id: int):
        url = f"{self.api}/v2/manage/placements/{placement_id}"

        return self.resource_util.get_resource_with_test_case_naming(
            placement_id, "placement", url, self.context.case_name
        )
