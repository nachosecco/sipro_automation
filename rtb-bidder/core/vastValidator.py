import xml.etree.ElementTree as ET


def count_ads(vast_xml):
    return len(vast_xml.findall("Ad"))


def get_vast_version(vast_xml):
    return vast_xml.get("version")


def get_impressions(ad):
    impressions = ad.findall("./InLine/Impression")
    if len(impressions) == 0:
        impressions = ad.findall("./Wrapper/Impression")
    return impressions


class VastValidator:
    def __init__(self, root_xml, rtb_response_validator):
        self.__vast_xml = ET.XML(root_xml)
        self.__rtb_response_validator = rtb_response_validator

    def back(self):
        """
        Use for chaining calls and assert back to rtb response
        """
        return self.__rtb_response_validator

    def ad_count_is(self, expected: int):
        value = count_ads(self.__vast_xml)
        assert (
            value == expected
        ), f"number of ads differs from expected:{expected} vs {value}"
        return self

    def vast_version_is(self, expected: str):
        value = get_vast_version(self.__vast_xml)
        assert (
            value == expected
        ), f"Vast version differs from expected:{expected} vs {value}"
        return self

    def is_empty(self):
        assert (
            len(self.__vast_xml.findall("*")) == 0
        ), f"vast xml was expected to be empty but was {self.__vast_xml}"
        return self

    def is_not_empty(self):
        assert (
            len(self.__vast_xml.findall("*")) > 0
        ), "vast xml was NOT expected to be empty but it was"
        return self

    def vast_xml(self):
        return self.__vast_xml
