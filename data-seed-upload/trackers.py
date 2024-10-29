from context import Context
from resourceUtil import ResourceUtil, sanitize
from trackersDefaultValues import DEFAULT_TRACKERS_BODY

TRACKERS = "/v2/manage/trackers"


def change_old_id_to_new_id_for_trackers(old_trackers_id, trackers):
    """It will return a new list of the correspondent new id trackers that equivalent of the olds ids"""
    new_trackers_id = []

    for old_tracker_id in old_trackers_id or []:
        new_tracker = trackers.get(old_tracker_id)
        if new_tracker is None:
            continue
        new_trackers_id.append(new_tracker.get("id"))

    return new_trackers_id


class Trackers:
    def __init__(self, context: type(Context)):
        self.resource_util = ResourceUtil(context)
        self.api = context.configuration.dashboard_api

    def upload(self, resources, trackers_serializations):
        trackers_response = {}

        url = f"{self.api}{TRACKERS}"
        trackers = resources.get("trackers")
        trackers_by_name = trackers.get("name")
        trackers_by_url = trackers.get("url_type")
        for tracker_serialization in trackers_serializations or []:
            tracker_serialization_id = tracker_serialization.get("id")
            tracker_serialization_url = tracker_serialization.get("url")
            tracker_serialization_type = tracker_serialization.get("type")

            # Trackers cannot be repeated by type and url,
            # so we check to see if it's already been created in the env before attempting to create it
            tracker_found_on_env = trackers_by_url.get(
                f"{tracker_serialization_url}{tracker_serialization_type}", None
            )

            if tracker_found_on_env is None:
                tracker_request = sanitize(tracker_serialization, ["description"])
                tracker_request["description"] = tracker_serialization.get("name")

                tracker_response = self.resource_util.sync(
                    url,
                    tracker_request,
                    trackers_by_name,
                    DEFAULT_TRACKERS_BODY,
                    "tracker",
                )

                trackers_response[tracker_serialization_id] = tracker_response
            else:
                trackers_response[tracker_serialization_id] = tracker_found_on_env
        return trackers_response
