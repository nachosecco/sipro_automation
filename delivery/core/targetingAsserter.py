import logging
from typing import List

from core.configuration import Configuration
from core.targeting import DeviceTargeting, GeoTargeting, MediaSizeTargeting
from core.vpc import VPC
from core.utils.stringUtils import subStringBetween


class GeoTargetingAsserter:
    """Class for assertion  of the geo targeting"""

    def __init__(self, saved_logs, vpc: VPC):

        self.log_found = self.__find_log_entry(saved_logs).strip()
        self.log_was_found = len(self.log_found) != 0
        self.vpc = vpc

    def isExpectedGeoInTheLog(self, expected_geo: type(GeoTargeting)):
        """This method is deprecated use is_expected_geo"""
        return self.is_expected_geo(expected_geo)

    def is_expected_geo(self, expected_geo: type(GeoTargeting)):
        """It will find the correct log, parse it and compare it to the expected geo class"""

        if not self.log_was_found:
            logging.error("The log for geo targeting was not found")
            return False

        found_geo = self.__parse_log(self.log_found)

        logging.info(
            f"Asserting that the expected geo values are :{repr(expected_geo)}"
            f" and vpc input ip is [{self.vpc.ip_address}] and the found geo values are: {repr(found_geo)}"
        )

        for attr, value in expected_geo.__dict__.items():
            value_found = getattr(found_geo, attr)
            if len(value) > 0 and value != value_found:
                logging.error(
                    f"The expected geo targeting {attr} value is {value} and the log value has {value_found}"
                )
                return False

        return True

    def assertGeo(self, geo: type(GeoTargeting)):
        """This method is deprecated use assert_geo"""
        return self.assert_geo(geo)

    def assert_geo(self, geo: type(GeoTargeting)):
        assert self.isExpectedGeoInTheLog(geo)

    @staticmethod
    def __find_log_entry(logs):
        for log in logs:
            if log.find("geoInfo") != -1:
                return log
        return ""

    # Parsing the log to have the information related to geo targeting
    @staticmethod
    def __parse_log(log: str):
        log = log.strip()
        found_geo = GeoTargeting()
        found_geo.country = subStringBetween(log, 'countryCode: "', '"')
        found_geo.region = subStringBetween(log, 'subCode: "', '"')
        found_geo.regionName = subStringBetween(log, 'subName: "', '"')
        found_geo.cityName = subStringBetween(log, 'cityName: "', '"')
        found_geo.postalCode = subStringBetween(log, 'postalCode: "', '"')
        found_geo.dma = subStringBetween(log, 'dma: "', '"')
        found_geo.city = subStringBetween(log, 'cityCode: "', '"')
        return found_geo


class DeviceTargetingAsserter:
    def __init__(self, logs, vpc: VPC):
        self.logs = logs
        self.vpc = vpc

    def isExpectedDeviceTargetingInTheLog(
        self, expected_device_targeting: type(DeviceTargeting)
    ):
        """Deprecated method use is_expected_device_targeting"""
        return self.is_expected_device_targeting(expected_device_targeting)

    def is_expected_device_targeting(
        self, expected_device_targeting: type(DeviceTargeting)
    ):
        log_found = self.__find_log_entry(self.logs).strip()
        if len(log_found) == 0:
            logging.error(
                f"The log message related to device targeting was not found in the logs, "
                f"so we cannot check the geo targeting"
            )
            return False

        found_device_targeting_in_log = self.__parse_log(log_found)

        logging.debug(
            f"Asserting that the expected device targeting values are : [{repr(expected_device_targeting)}]"
            f" , vpc user agent is [{self.vpc.ua}]"
            f" and the found device targeting values are: [{repr(found_device_targeting_in_log)}]"
        )

        for attr, value in expected_device_targeting.__dict__.items():
            value_found = getattr(found_device_targeting_in_log, attr)
            if len(value) > 0 and value != value_found:
                logging.error(
                    f"The expected device targeting {attr}  value is [{value}] and the log value has [{value_found}]"
                )
                return False

        return True

    # Parsing the log to have the information related to geo targeting
    @staticmethod
    def __parse_log(log: str):
        device = DeviceTargeting()
        device.type = subStringBetween(log, "deviceType: ", " ")
        device.os = subStringBetween(log, "deviceOS: ", " ")
        device.version = subStringBetween(log, 'deviceVersion: "', '"')
        device.vendor = subStringBetween(log, 'deviceMake: "', '"')
        device.model = subStringBetween(log, 'deviceModel: "', '"')
        return device

    @staticmethod
    def __find_log_entry(logs):
        for log in logs:
            if log.find("Sending Event:VIDEOTRUEFIRSTCALL") != -1:
                return log
        return ""


class AudienceTargetingAsserter:
    def __init__(self, logs):
        self.logs = logs

    def assert_blocked(self):
        found_value = False
        for log in self.logs:
            if "NOT_MATCHED - Blocked" in log:
                found_value = True
        assert found_value

    def assert_pass(self, expected_cpm=None, expected_audience_ids=None):
        found_log = None
        for log in self.logs:
            if "MATCHED - Not blocked" in log:
                found_log = log

        if found_log is None:
            logging.error(
                "Audience Targeting, The log not blocked, was not found, check if is blocked"
            )
            assert False

        if not (expected_cpm is None):
            found_cpm = subStringBetween(found_log, "cpm ", ",")

            if not (found_cpm == str(expected_cpm)):
                logging.error(
                    "Audience Targeting, The expected cpm value is %s and the found value is %s",
                    str(expected_cpm),
                    found_cpm,
                )
                assert False
        if not (expected_audience_ids is None):
            audience_log_values = found_log.split("ids ")
            found_audience_ids = audience_log_values[1]

            if found_audience_ids != expected_audience_ids:
                logging.error(
                    "Audience Targeting, The expected audienceIds value is %s and the found value is %s",
                    expected_audience_ids,
                    found_audience_ids,
                )
                assert False


class MediaSizeTargetingAsserter:
    def __init__(self, xml_root, configuration: type(Configuration)):
        self.xml_root = xml_root
        self.configuration = configuration

    def expect(self, expected_media_sizes: List[MediaSizeTargeting]):
        """This will assert that all media sizes targeting are in vast, it won't check the order of the vast"""

        url_prefix = f"{self.configuration.media_server_path}/media/"
        used = []

        expected = []
        for expected_media_size in expected_media_sizes:
            url_suffix = expected_media_size.to_value()
            url = f"{url_prefix}{url_suffix}"
            expected.append(url)
        expected_not_found = expected.copy()
        media_urls = self.xml_root.findall(".//MediaFile")
        media_urls_found = []
        for media_url in media_urls:
            media_urls_found.append(media_url.text)

            for expected_media_size in expected_not_found:

                if expected_media_size == media_url.text:
                    used.append(expected_media_size)

            expected_not_found = [x for x in expected_not_found if x not in used]
        if len(expected_not_found) > 0:
            logging.error(
                f"It was not found the expected media targeting size {expected} "
                f"the found urls were {media_urls_found}"
            )
            assert False


class TargetingAsserter:
    def __init__(
        self, xml_root, saved_logs, configuration: type(Configuration), vpc: VPC
    ):
        self.xml_root = xml_root
        self.logs = saved_logs
        self.vpc = vpc
        self.configuration = configuration

    def geo(self):
        return GeoTargetingAsserter(self.logs, self.vpc)

    def device(self):
        return DeviceTargetingAsserter(self.logs, self.vpc)

    def audience(self):
        return AudienceTargetingAsserter(self.logs)

    def media_size(self):
        return MediaSizeTargetingAsserter(self.xml_root, self.configuration)
