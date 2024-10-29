import logging
import xml.etree.ElementTree as ET

from core.adPodAssertor import adPodAssertor
from core.assertor.cookieAssertor import CookieAssertor
from core.assertor.eventAppLogsAssertor import EventAppLogsAssertor
from core.assertor.eventAsserter import EventAsserter
from core.case import Case
from core.configuration import Configuration
from core.enums.filterReason import FilterReason
from core.filterAssertor import FilterAssertor
from core.logReader import LogReader, SavedLogReader
from core.rtbBidRequestValidator import RtbBidRequestValidator
from core.targetingAsserter import TargetingAsserter
from core.validator.responseHeadersValidator import ResponseHeadersValidator
from core.validator.rtb_auction_validator import RtbAuctionValidator
from core.validator.vastImpressionTagValidator import VastImpressionTagValidator
from core.validator.vastMediaTagValidator import VastMediaTagValidator
from core.vpc import VPC
from core.assertor.extensionAssertor import AdExtensionAsserter


class VastXMLAsserter:
    def __init__(self, vast_xml, root_xml, configuration=Configuration()):
        self.vast_xml = vast_xml
        self.root_element_xml = root_xml
        self.configuration = configuration

    def __found_media_duration(self):
        ads = self.root_element_xml.findall("Ad")
        for ad in ads:
            duration_vast = ad.find("./InLine/Creatives/Creative/Linear/Duration")
            if duration_vast is None:
                duration_vast = ad.find("./Wrapper/Creatives/Creative/Linear/Duration")
            duration = duration_vast.text
            logging.info(f"duration: {duration}")
            return duration

    def assertDuration(self, duration):
        vast_duration = self.__found_media_duration()
        if duration != vast_duration:
            logging.error(
                f"The expected duration is [{duration}]  and was found [{vast_duration}]"
            )
        assert duration == self.__found_media_duration()

    def assertAdsCount(self, expected_length: int):
        """Deprecated use assert_ad_count"""
        return self.assert_ad_count(expected_length)

    # Count the ads in response of the vast
    def assert_ad_count(self, expected_length: int):
        ads_counts = self.__count_ads()
        if expected_length != ads_counts:
            logging.error(
                f"The expectedLength is [{expected_length}] and was found [{ads_counts}]"
            )
        assert expected_length == ads_counts

    def assert_creatives_is_url_in_media_server(self):
        creatives = self.root_element_xml.findall(".//MediaFile")
        media_server_path = self.configuration.media_server_path
        for creative in creatives:
            vast_creative_url = creative.text

            if not (vast_creative_url.startswith(self.configuration.media_server_path)):
                logging.error(
                    f"The creative_url url {vast_creative_url} "
                    f"don't start with the expected server {media_server_path}"
                )
                assert False

    def __count_ads(self):
        return len(self.root_element_xml.findall("Ad"))

    # Checks for impression roll event in the vast response

    def assert_impression_roll_event(self):

        ads = self.root_element_xml.findall("Ad")
        for ad in ads:
            found_event_roll_impression = False
            impressions = get_impressions(ad)
            ad_id = ad.get("id")

            logging.info(
                f"There are {len(impressions)} tags of Impression in the ad {ad_id}"
            )

            for impression in impressions:

                if "ev=rollimp" in impression.text:
                    found_event_roll_impression = True

            if not found_event_roll_impression:
                logging.error(
                    f"The event of impression `ev=rollimp` was not found in the ad {ad_id}"
                )
                assert False

    # This would check that all tracking events are in the vast response.
    def assert_all_tracking_events(self):
        trackers = {"start", "firstQuartile", "midpoint", "thirdQuartile", "complete"}
        tag_tracking = self.root_element_xml.findall(
            "./Ad/InLine/Creatives/Creative/Linear/TrackingEvents/Tracking"
        )
        if len(tag_tracking) == 0:
            self.root_element_xml.findall(
                "./Ad/Wrapper/Creatives/Creative/Linear/TrackingEvents/Tracking"
            )

        for tracking in tag_tracking:
            event = tracking.get("event")

            if event is None:
                logging.error(
                    "There is problem related to the event in the vast response."
                )
                assert False
            if not (event in trackers):
                logging.error("The event " + event + " please check the vast response.")
                assert False

    def assertTagImpressionContainsText(self, text_to_find: str):
        ads = self.root_element_xml.findall("Ad")
        for ad in ads:
            impressions = get_impressions(ad)
            found_text_in_tag_impression = False
            for impression in impressions:
                if text_to_find in impression.text:
                    found_text_in_tag_impression = True

            if not found_text_in_tag_impression:
                logging.error(
                    f"The text({text_to_find}) was not found in the tags of impression in the vast"
                )

            assert found_text_in_tag_impression

    def assertTagImpressionNotContainsText(self, textToFind: str):
        ads = self.root_element_xml.findall("Ad")
        for ad in ads:
            impressions = get_impressions(ad)
            foundTextInTagImpression = False
            for impression in impressions:
                if textToFind in impression.text:
                    foundTextInTagImpression = True

            if foundTextInTagImpression:
                logging.error(
                    f"The text({textToFind}) was found in the tags of impression in the vast"
                )

            assert not foundTextInTagImpression

    def assertVastVersion(self, version: str):
        actual_version = self.__get_vast_version()
        if version == actual_version:
            logging.info("Valid VAST version %s", version)
        else:
            logging.error(
                f"Vast version expected was {version} but received in response is {actual_version}"
            )
        assert version == actual_version

    def __get_vast_version(self):
        return self.root_element_xml.get("version")

    def assertMediaTags(self):
        return VastMediaTagValidator(self.root_element_xml)

    def assert_not_empty(self):
        assert len(self.root_element_xml.findall("*")) > 0

    def assertTrackerTags(self, tracker_hostname: str):
        return VastImpressionTagValidator(self.root_element_xml, tracker_hostname)

    def getAllImpressions(self):
        ads = self.root_element_xml.findall("Ad")
        impressions = []
        for ad in ads:
            for impression in get_impressions(ad):
                impressions.append(impression.text)
        return impressions


# Class that is to assert all that is necessary in a test case.
class VastResultAssertor:
    def __init__(
        self,
        vastXML,
        status: int,
        vpc: VPC,
        directoryPathVastResponse: str,
        response_headers,
        configOverride: Configuration = None,
    ):

        self.xml = vastXML
        self.status: int = status
        self.xmlRoot: ET.Element = None if self.xml is None else self.xml.getroot()
        self.vpc = vpc
        self.directoryPathVastResponse = directoryPathVastResponse
        self.logReader = LogReader(self.vpc, configOverride)
        self.eventLogs = None
        self.responseHeaders = response_headers
        self.configuration = configOverride or Configuration()

    def assertLogsDelivery(self, containsToTest):
        """deprecated use assert_logs_delivery"""
        return self.assert_logs_delivery(containsToTest)

    def assert_logs_delivery(self, contains_to_test):
        if isinstance(contains_to_test, str):
            contains_to_test = contains_to_test.split(",")
        assert self.logReader.read_delivery(contains_to_test)

    def assert_logs_events(self, contains_to_test):
        if len(contains_to_test) > 0:
            self.eventLogs = self.logReader.find_logs_events()
            assert self.logReader.read_events(contains_to_test, self.eventLogs)

    # Runs all assertions in the case file and standard assertions
    def assert_case(self, case: Case):
        if len(case.logDelivery) > 0:
            logging.info("Expected Delivery logs " + str(case.logDelivery))

        self.assertLogsDelivery(case.logDelivery)
        self.assert_logs_events(case.logEvents)

        if self.status == 200:
            vast_response_asserter = self.assertXML()

            vast_response_asserter.assert_impression_roll_event()
            vast_response_asserter.assert_all_tracking_events()

    # Runs all assertions in the case file and standard assertions
    def assertCase(self, case: Case):
        """Deprecated use assert_case"""
        self.assert_case(case)

    def assert_vast_xml(self):
        return VastXMLAsserter(self.xml, self.xmlRoot, self.configuration)

    def assertXML(self):
        """Deprecated use assert_vast_xml"""
        return self.assert_vast_xml()

    def deliveryLogs(self):
        """Deprecated use `delivery_logs`"""
        return self.delivery_logs()

    def delivery_logs(self):
        logs = self.logReader.find_logs_delivery()
        return SavedLogReader("delivery", self.directoryPathVastResponse, logs)

    def event_logs(self):
        logs = self.logReader.find_logs_events()
        return SavedLogReader("event", self.directoryPathVastResponse, logs)

    def assertTargeting(self):
        """Deprecated use assert_targeting"""
        return self.assert_targeting()

    def assert_targeting(self):
        return TargetingAsserter(
            self.xmlRoot, self.deliveryLogs().logs, self.configuration, self.vpc
        )

    def assertAdPod(self):
        """Deprecated use assert_adpod"""
        return self.assert_adpod()

    def assert_adpod(self):
        return adPodAssertor(self.xml, self.vpc)

    def assertFilter(self, filter_reason: FilterReason):
        """Deprecated use assert_filter"""
        return self.assert_filter(filter_reason)

    def assert_filter(self, filter_reason: FilterReason):
        return FilterAssertor(
            self.deliveryLogs().logs, self.vpc, filter_reason
        ).validate_reason()

    def validate_filter_reason(self, filter_reason: FilterReason):
        return FilterAssertor(self.deliveryLogs().logs, self.vpc, filter_reason)

    def validate_rtb_bid_request(self):
        return RtbBidRequestValidator(self.deliveryLogs().logs)

    def validate_rtb_auction(self):
        return RtbAuctionValidator(self.deliveryLogs().logs)

    def validate_headers(self):
        return ResponseHeadersValidator(self.responseHeaders)

    def assert_event(self):
        return EventAsserter(self.delivery_logs().logs, self.vpc)

    def assertEvent(self):
        """Deprecated use assert_event"""
        return self.assert_event()

    def assertEventAppLog(self):
        """deprecated use assert_event_log"""
        return self.assert_event_log()

    def assert_event_log(self):
        return EventAppLogsAssertor(self.eventLogs, self.vpc)

    def assertCookie(self, startsWith="UserCookie(", endsWith="), geoCookie"):
        """deprecated use assert_cookie"""
        return self.assert_cookie(startsWith, endsWith)

    def assert_cookie(self, starts_with="UserCookie(", ends_with="), geoCookie"):
        return CookieAssertor(self.deliveryLogs().logs).parse_cookie_log(
            starts_with, ends_with
        )

    def assert_extension(self):
        return AdExtensionAsserter(self.xmlRoot)


def get_impressions(ad):
    impressions = ad.findall("./InLine/Impression")
    if len(impressions) == 0:
        impressions = ad.findall("./Wrapper/Impression")
    return impressions
