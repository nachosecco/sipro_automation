import logging

from context import Context
from resourceUtil import ResourceUtil


class Tracker:
    def __init__(self, context: type(Context), trackers):
        self.context = context
        self.logger = logging.getLogger("extractor")
        self.trackers = trackers
        self.resource_util = ResourceUtil(context.authorization_context)
        self.api = self.context.configuration.dashboard_api

    def extract(self):
        case_name = self.context.case_name
        trackers = []
        base_url = f"{self.api}/v2/manage/trackers/"

        for tracker_id in self.trackers:
            url = f"{base_url}{tracker_id}"
            tracker = self.resource_util.get_resource_with_test_case_naming(
                tracker_id, "tracker", url, case_name
            )
            trackers.append(tracker)
        return self.resource_util.resource_name_for_collection(
            case_name, "tracker", trackers
        )
