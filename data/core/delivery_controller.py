import logging
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import List

import requests

from core.dashboard.dashboard_placements_api import fetch_aligned_medias
from core.data_exception import DataException
from core.event_url_holder import EventUrlsHolder


class CommonController(ABC):
    """Abstract class to abstract behavior downstream"""

    @abstractmethod
    def generate_url(self):
        pass

    @abstractmethod
    def call_for_delivery_and_generate_opportunity(self) -> List[EventUrlsHolder]:
        pass

    def request(self) -> List[EventUrlsHolder]:
        return self.call_for_delivery_and_generate_opportunity()


def contains_rollimp(input_string: str) -> bool:
    return "ev=rollimp" in input_string


def get_tracking_urls(holder):
    tracking_events = holder.find("Creatives/Creative/Linear/TrackingEvents")

    start = tracking_events.find("Tracking[@event='start']").text
    first_quartile = tracking_events.find("Tracking[@event='firstQuartile']").text
    midpoint = tracking_events.find("Tracking[@event='midpoint']").text
    third_quartile = tracking_events.find("Tracking[@event='thirdQuartile']").text
    complete = tracking_events.find("Tracking[@event='complete']").text

    return start, first_quartile, midpoint, third_quartile, complete


def get_click_url(holder) -> str:
    return holder.find("Creatives/Creative/Linear/VideoClicks/ClickTracking").text


class VPCController(CommonController):
    """Will prepare the url call for the opportunity
    and parse a vast"""

    def __init__(self, case):
        self.case = case
        self.base_url = case.configuration.get_delivery_url()

    def generate_url(self) -> str:
        return self.base_url + "/vast?" + self.case.delivery_parameters.query_params()

    def get_media_name(self, medias: list, uid: str):
        for media in medias:
            if media.get("guid") == uid:
                return media.get("name")

        raise DataException(
            f"Media {uid} is not aligned to {self.case.delivery_parameters.uid}."
        )

    def do_call_delivery(self):
        # this method should call for delivery
        # with the returned vast should populate event url holder
        full_url = self.generate_url()
        logging.info(f"Calling delivery: {full_url}")
        response = requests.get(full_url, timeout=120)
        if not response.status_code == 200:
            logging.warning(
                f"The status code of the request was {response.status_code}"
            )
            raise DataException(
                f"Got non-200 status code {response.status_code}, for url: {full_url}."
            )
        logging.info(f"/vast success for: {self.case.delivery_parameters.uid}")

        return response

    def call_for_delivery_and_generate_opportunity(self) -> [EventUrlsHolder]:

        xml = ET.ElementTree(ET.fromstring(self.do_call_delivery().text))
        events = []
        aligned_medias = fetch_aligned_medias(
            self.case.get_authorization_context(), self.case.delivery_parameters.uid
        )
        for ad in xml.findall("./Ad"):
            ad_id = ad.attrib.get("id")
            media_name = self.get_media_name(aligned_medias, ad_id)
            holder = ad.find("Wrapper")
            if holder is None:
                holder = ad.find("InLine")
            impression_url = holder.find("Impression").text

            # We are only interested if it has ev=rollimp
            if not contains_rollimp(impression_url):
                continue

            (
                start,
                first_quartile,
                midpoint,
                third_quartile,
                complete,
            ) = get_tracking_urls(holder)
            click = get_click_url(holder)
            event = EventUrlsHolder(
                ad_id,
                media_name,
                impression_url,
                start,
                first_quartile,
                midpoint,
                third_quartile,
                complete,
                click,
            )
            events.append(event)

        return events


class DisplayFilterController(CommonController):
    """Will prepare the url call for the opportunity
    and parse a vast"""

    def __init__(self, case):
        self.case = case
        self.base_url = case.configuration.get_delivery_url()

    def generate_url(self):
        return self.case.delivery_parameters.generate_url(self.base_url)

    def call_for_delivery_and_generate_opportunity(self):
        # this method should call for delivery
        # with the returned vast should populate event url holder

        events_ad_1 = EventUrlsHolder(
            "id",
            "media_name",
            "impression_url",
            "start_url",
            "firstQuartile_url",
            "midpointUrl",
            "thirdQuartile_url",
            "complete_url",
            "click_url",
        )
        events_ad_2 = EventUrlsHolder(
            "id2",
            "media_name",
            "impression_url2",
            "start_url",
            "firstQuartile_url",
            "midpointUrl",
            "thirdQuartile_url",
            "complete_url",
            "click_url",
        )
        return [events_ad_1, events_ad_2]


class VpaidFilterController(CommonController):
    """Will prepare the url call for the opportunity
    and parse a vast"""

    def __init__(self, case):
        self.case = case

    def generate_url(self):
        return ""

    def call_for_delivery_and_generate_opportunity(self):
        # this method should call for delivery
        # with the returned vast should populate event url holder
        events_ad_1 = EventUrlsHolder(
            "id",
            "media_name",
            "impression_url",
            "start_url",
            "firstQuartile_url",
            "midpointUrl",
            "thirdQuartile_url",
            "complete_url",
            "click_url",
        )
        return [events_ad_1]


class DeliveryControllers:
    """Class that based on type of placement will use the controller for that class"""

    def __init__(self, case):
        self.case = case

    def ctv(self):
        return VPCController(self.case)

    def intstream(self):
        return VPCController(self.case)

    def display(self):
        return DisplayFilterController(self.case)

    def vpaid(self):
        return VpaidFilterController(self.case)
