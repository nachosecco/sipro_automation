import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    """Testing 2 media with the same cpm
One of the media has priority of 1 and weight of 1. The other media has priority of 2 and weight of 1,
the media with 1-1 should be the first in the vast
"""
)
def test_media_with_same_cpm_and_company_priority_type_by_priority():
    case = Case("test_media_with_same_cpm_and_company_priority_type_by_priority")
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # checking we have 2 ads
    vast_result.assert_vast_xml().assert_ad_count(2)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    # the first ad should have a text with "priority-1-1-highest" as part of the uri
    first_uri = ads[0].find("./Wrapper/VASTAdTagURI").text
    if "priority-1-1-highest" not in first_uri:
        logging.error(
            "The first ad should have the text 'priority-1-1-highest' as part of the tag"
        )
        assert False

    # the second ad it should a text with "priority-2-1-lower" as part of the uri
    second_uri = ads[1].find("./Wrapper/VASTAdTagURI").text
    if "priority-2-1-lower" not in second_uri:
        logging.error(
            "The second ad should have the text 'priority-2-1-lower' as part of the tag"
        )
        assert False


@pytest.mark.regression
@description(
    """Testing 2 media with the same priority and weight
One of the media has cpm of 20. The other media has cpm of 5
the media with higher-cpm-20 should be the first in the vast
"""
)
def test_media_with_same_priority_and_weight_and_company_priority_type_by_priority():
    case = Case(
        "test_media_with_same_priority_and_weight_and_company_priority_type_by_priority"
    )
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # checking we have 2 ads
    vast_result.assert_vast_xml().assert_ad_count(2)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    # the first ad should have a text with higher-cpm-20 as part of the uri
    first_uri = ads[0].find("./Wrapper/VASTAdTagURI").text
    if "higher-cpm-20" not in first_uri:
        logging.error(
            "The first ad should have the text 'higher-cpm-20' as part of the tag"
        )
        assert False

    # the second ad it should a text with low-cpm-5 as part of the uri
    second_uri = ads[1].find("./Wrapper/VASTAdTagURI").text
    if "low-cpm-5" not in second_uri:
        logging.error(
            "The second ad should have the text 'low-cpm-5' as part of the tag"
        )
        assert False


def count_found_tags(ad, found_tags):
    tag_url = ad.find("./Wrapper/VASTAdTagURI")
    tag_executed = found_tags.get(tag_url.text, 0) + 1
    found_tags[tag_url.text] = tag_executed


def assert_found_tags(found_tags):
    for v in found_tags.values():
        if v < 10 or v > 30:
            logging.error(
                "The tags values %s are are not between the expected targets (>=10 & <=30"
                "The config of the media are all back-fill so it should be somewhat similar",
                found_tags.values(),
            )
            assert False


@pytest.mark.regression
@description(
    """Testing 3 media with the same priority and weight and cpm
The order should change
"""
)
def test_media_with_same_priority_and_cpm_and_weight_and_random_order():
    case = Case("test_media_with_same_priority_and_cpm_and_weight_and_random_order")
    vpc = case.vpc

    executions = range(50)
    found_tags_first_position = {}
    found_tags_second_position = {}
    found_tags_third_position = {}

    for _ in executions:
        vpc.regenerate_automation_framework()

        vast_result = VastValidator().test(vpc)

        vast_result.assert_vast_xml().assert_ad_count(3)

        ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

        count_found_tags(ads[0], found_tags_first_position)
        count_found_tags(ads[1], found_tags_second_position)
        count_found_tags(ads[2], found_tags_third_position)

    assert_found_tags(found_tags_first_position)
    assert_found_tags(found_tags_second_position)
    assert_found_tags(found_tags_third_position)
