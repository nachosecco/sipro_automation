import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    """Testing 2 media with the same priority
of a media of CPM of 10 or a media of CPM of 20, the media with 20 CPM should be first in the vast
"""
)
def test_media_with_same_priority_and_company_priority_type_by_cpm():
    case = Case("test_media_with_same_priority_and_company_priority_type_by_cpm")
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # checking we have 2 ads
    vast_result.assert_vast_xml().assert_ad_count(2)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    # the first ad should have a 20 cpm as part of the uri
    first_uri = ads[0].find("./Wrapper/VASTAdTagURI").text
    if "media_cpm_20" not in first_uri:
        logging.error("The first ad should have text with 'media_cpm_20' in the tag")
        assert False

    # the second ad it should a 10 cpm as part of the uri
    second_uri = ads[1].find("./Wrapper/VASTAdTagURI").text
    if "media_cpm_10" not in second_uri:
        logging.error("The second ad should have text with 'media_cpm_10' in the tag")
        assert False


@pytest.mark.regression
@description(
    """Testing 2 media with the different priority
with CPM 20 and 30 then the media with the highest cpm should be the first in the vast response
"""
)
def test_media_with_with_highest_cpm_in_lowest_priority_with_priority_type_by_cpm():
    case = Case(
        "test_media_with_with_highest_cpm_in_lowest_priority_with_priority_type_by_cpm"
    )
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # checking we have 2 ads
    vast_result.assert_vast_xml().assert_ad_count(2)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    # The first ad should have a 30 cpm as part of the uri
    first_uri = ads[0].find("./Wrapper/VASTAdTagURI").text
    if "media_cpm_30" not in first_uri:
        logging.error("The first ad should have a 20 cpm if is using lower priority")
        assert False

    # the second ad should have a 20 cpm as part of the uri
    second_uri = ads[1].find("./Wrapper/VASTAdTagURI").text
    if "media_cpm_20" not in second_uri:
        logging.error("The second ad should have a 10 cpm if is using higher priority")
        assert False


@pytest.mark.regression
@description(
    """Testing 2 media with different priority
of a media of CPM (20) cpm then highest priority should be first in the vast
"""
)
def test_media_with_different_priority_and_same_cpm_and_with_priority_type_by_cpm():
    case = Case(
        "test_media_with_different_priority_and_same_cpm_and_with_priority_type_by_cpm"
    )

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # checking we have 2 ads
    vast_result.assert_vast_xml().assert_ad_count(2)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    # the first ad it should highest as part of the uri
    first_uri = ads[0].find("./Wrapper/VASTAdTagURI").text
    if "highest" not in first_uri:
        logging.error("The first ad should have the text 'highest' as part of the tag")
        assert False

    # the second ad it should a 20 cpm as part of the uri
    second_uri = ads[1].find("./Wrapper/VASTAdTagURI").text
    if "lowest" not in second_uri:
        logging.error("The second ad should have the text 'lowest' as part of the tag")
        assert False


@pytest.mark.regression
@description(
    """Testing 2 media with different priority, 1 with high and 1 with back fill
of a media of CPM (20) cpm then highest priority should be the first in the vast
"""
)
def test_media_with_back_fill_vs_priority_and_same_cpm_and_with_priority_type_by_cpm():
    case = Case(
        "test_media_with_back_fill_vs_priority_and_same_cpm_and_with_priority_type_by_cpm"
    )

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # checking we have 2 ads
    vast_result.assert_vast_xml().assert_ad_count(2)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    #  the first ad should have the text "highest" as part of the uri
    first_uri = ads[0].find("./Wrapper/VASTAdTagURI").text
    if "highest" not in first_uri:
        logging.error("The first ad should have text 'highest' as part of the tag")
        assert False

    # the second ad should have the text "backfill" as part of the uri
    second_uri = ads[1].find("./Wrapper/VASTAdTagURI").text
    if "backfill" not in second_uri:
        logging.error(
            "The second ad should have the text 'backfill' as part of the tag"
        )
        assert False


@pytest.mark.regression
@description(
    """Testing 2 media with different priorities, 1 with high and 1 with back-fill in weight
of a media of 20 cpm then highest priority should be the first in the vast
"""
)
def test_media_with_back_fill_weight_vs_priority_and_same_cpm_and_with_priority_type_by_cpm():
    case = Case(
        "test_media_with_back_fill_weight_vs_priority_and_same_cpm_and_with_priority_type_by_cpm"
    )

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # checking we have 2 ads
    vast_result.assert_vast_xml().assert_ad_count(2)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")

    # the first ad should "highest" as part of the uri
    first_uri = ads[0].find("./Wrapper/VASTAdTagURI").text
    if "highest" not in first_uri:
        logging.error("The first ad should have the text 'highest' as part of the tag")
        assert False

    # the second ad should have the text "backfill" as part of the uri
    second_uri = ads[1].find("./Wrapper/VASTAdTagURI").text
    if "backfill" not in second_uri:
        logging.error("The second ad should have 'backfill' as part of the tag")
        assert False
