import json
import logging
from datetime import datetime
from pathlib import Path

import requests
from requests import Response

from core.delivery_controller import CommonController
from core.delivery_events import DeliveryEvents
from core.event_url_holder import EventUrlsHolder


# pylint: disable=too-few-public-methods
class EventCoordinator:
    """Will call delivery using call back controller
    and then have the list of possible events to be called"""

    def __init__(self, case, controller: CommonController):
        self.case = case
        self.controller = controller
        self.min_date_time = None
        self.max_date_time = None
        self.total_events = 0

    def call_delivery(self, number_of_times: int = 1) -> DeliveryEvents:
        events = []
        events_callers = []
        for i in range(number_of_times):
            logging.info("calling %s of %s", i, number_of_times)
            ans = self.controller.request()
            events.extend(ans)

        for event in events:
            events_callers.append(EventCaller(event, self))
        return DeliveryEvents(events_callers)

    def call_event(self, url: str, event_type: str) -> Response:
        if self.min_date_time is None:
            self.min_date_time = datetime.now()

        logging.info(f"Calling {event_type} event: {url}")
        res = requests.get(url, timeout=10000)
        if res.status_code != 200:
            logging.error(f"Got {res.status_code} for {event_type} event: {url}")

        now = datetime.now()
        if self.max_date_time is None or now > self.max_date_time:
            self.max_date_time = now

        self.total_events += 1
        self.update_event_for_case()
        return res

    def call_events(self, event_type: str, url: str, number_of_event: int = 1):
        logging.info(f"Will call n[%s] {event_type} for URL: %s", number_of_event, url)
        for _ in range(number_of_event):
            self.call_event(url, event_type)

    def update_event_for_case(self):

        # creating parent dirs, of the path of events
        Path(self.case.configuration.path_case_events).mkdir(
            parents=True, exist_ok=True
        )

        path = (
            self.case.configuration.path_case_events
            + "/"
            + self.case.case_name_execution
            + ".json"
        )
        with open(path, "w") as event_file:
            json.dump(
                {
                    "case": self.case.case_name_execution,
                    "min_date": str(self.min_date_time),
                    "max_date": str(self.max_date_time),
                },
                event_file,
            )


class EventCaller:
    """Class that will prepare all events and then call it in the order that was prepared"""

    def __init__(self, data: EventUrlsHolder, event_coordinator: EventCoordinator):
        self.event_coordinator = event_coordinator
        self.data = data

    def call_impression(self, number_of_event: int = 1):
        self.event_coordinator.call_events(
            "impression", self.data.impression, number_of_event
        )
        return self

    def call_click(self, number_of_event: int = 1):
        self.event_coordinator.call_events("click", self.data.click, number_of_event)

    def call_beacon_start(self, number_of_event: int = 1):
        self.event_coordinator.call_events(
            "beacon-start", self.data.start, number_of_event
        )
        return self

    def call_beacon_first_quartile(self, number_of_event: int = 1):
        self.event_coordinator.call_events(
            "beacon-first_quartile", self.data.firstQuartile, number_of_event
        )
        return self

    def call_beacon_midpoint(self, number_of_event: int = 1):
        self.event_coordinator.call_events(
            "beacon-midpoint", self.data.midpoint, number_of_event
        )
        return self

    def call_beacon_third_quartile(self, number_of_event: int = 1):
        self.event_coordinator.call_events(
            "beacon-third_quartile", self.data.thirdQuartile, number_of_event
        )
        return self

    def call_beacon_complete(self, number_of_event: int = 1):
        self.event_coordinator.call_events(
            "beacon-complete", self.data.complete, number_of_event
        )
        return self
