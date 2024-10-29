import logging
from urllib.parse import urlparse, parse_qs

import pytest
from core.case import Case
from core.Description import description
from core.devices import DEVICE_CTV_ROKU
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "This is a case to check parameters that have whitespace in leading or trailing are ignored"
)
def test_incoming_parameters_with_space_ignored():
    case = Case("test_incoming_parameters_with_space_ignored")

    vpc = case.vpc

    vpc.player_width = " 640 "
    vpc.player_height = " 480 "
    vpc.ip_address = " 63.84.14.1 "

    vpc.ua = f" {DEVICE_CTV_ROKU.ua} "
    vpc.app_name = " disney_plus "
    vpc.pod_size = " 1 "
    vpc.pod_max_dur = " 120 "
    vpc.pod_min_ad_dur = " 1 "
    vpc.pod_max_ad_dur = " 120 "
    vpc.channel_name = " disney "
    vpc.network_name = " disney "
    vpc.content_series = " X-Men '97 "
    vpc.content_genre = " Superhero "
    vpc.content_len = " 20 "

    vast_result = VastValidator().test(vpc)

    # This will execute the all generic assertions in the case
    vast_result.assert_case(case)

    vast_xml = vast_result.assert_vast_xml().root_element_xml

    ad_tag_element = vast_xml.find("./Ad/Wrapper/VASTAdTagURI")

    if ad_tag_element.text == "":
        logging.error("Ad tag is empty")
        assert False

    ad_tag = ad_tag_element.text
    tag_values = urlparse(ad_tag, allow_fragments=True)

    query_params = parse_qs(tag_values.query)

    for attribute in vars(vpc):
        if not (attribute.startswith("_") or attribute == "uid"):
            value = getattr(vpc, attribute)
            if not (value == "[REPLACE]" or value is None):
                clean_value = value.rstrip().lstrip()
                tag_values = query_params.get(attribute)
                if tag_values is None:
                    logging.warning("The key %s is not in the ad tag", attribute)
                else:

                    tag_value = query_params.get(attribute)[0]
                    if not clean_value == tag_value:
                        logging.error(
                            "The key %s as leading or trailing whitespace "
                            "tag value = [%s] expected value [%s]",
                            attribute,
                            tag_value,
                            clean_value,
                        )
                        assert False


def test_incoming_parameters_with_tab_ignored():
    case = Case("test_incoming_parameters_with_tab_ignored")

    vpc = case.vpc

    vpc.player_width = "	640		"
    vpc.player_height = "	480	"
    vpc.ip_address = "	63.84.14.1	"

    vpc.ua = f"	{DEVICE_CTV_ROKU.ua}	"
    vpc.app_name = "	disney_plus	"
    vpc.pod_size = "	1	"
    vpc.pod_max_dur = "	120	"
    vpc.pod_min_ad_dur = "	1	"
    vpc.pod_max_ad_dur = "	120	"
    vpc.channel_name = "	disney	"
    vpc.network_name = "	disney	"
    vpc.content_series = "	X-Men '97	"
    vpc.content_genre = "	Superhero	"
    vpc.content_len = "	20	"

    vast_result = VastValidator().test(vpc)

    # This will execute the all generic assertions in the case
    vast_result.assert_case(case)

    vast_xml = vast_result.assert_vast_xml().root_element_xml

    ad_tag_element = vast_xml.find("./Ad/Wrapper/VASTAdTagURI")

    if ad_tag_element.text == "":
        logging.error("Ad tag is empty")
        assert False

    ad_tag = ad_tag_element.text
    tag_values = urlparse(ad_tag, allow_fragments=True)

    query_params = parse_qs(tag_values.query)

    for attribute in vars(vpc):
        if not (attribute.startswith("_") or attribute == "uid"):
            value = getattr(vpc, attribute)
            if not (value == "[REPLACE]" or value is None):
                clean_value = value.rstrip().lstrip()
                tag_values = query_params.get(attribute)
                if tag_values is None:
                    logging.warning("The key %s is not in the ad tag", attribute)
                else:

                    tag_value = query_params.get(attribute)[0]
                    if not clean_value == tag_value:
                        logging.error(
                            "The key %s as leading or trailing whitespace "
                            "tag value = [%s] expected value [%s]",
                            attribute,
                            tag_value,
                            clean_value,
                        )
                        assert False
