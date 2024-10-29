import pytest
from core.case import Case
from core.enums.filterReason import FilterReason

from core.Description import description
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    """Test that a media with custom url param targeting filters only requests that do not match rule

    We've set up a single placement with a single media aligned that has custom url targeting:
        * content_title of either "*Pet Detective" or "Ace Ventura*"
        * content_genre of "Comedy"
    """
)
def test_media_targeting_custom_url_expression():
    case = Case("test_media_targeting_custom_url_expression")
    vpc = case.vpc

    # We make our first request with params that are not a match
    vpc.content_title = "Not A Match"
    vpc.content_genre = "Horror"

    vast_result = VastValidator().test(vpc)

    # The media should be filtered and not included in the vast
    vast_result.assert_filter(FilterReason.TARGETING_PARAMS)
    vast_result.assert_vast_xml().assert_ad_count(0)

    # Set up VPC to make a second request that is a match
    vpc.regenerate_automation_framework()

    # Add params that match the rule
    vpc.content_title = "Ace Ventura: When Nature Calls"
    vpc.content_genre = "Comedy"

    vast_result = VastValidator().test(vpc)

    # If there's one media in the vast we know our only aligned media passed targeting checks.
    vast_result.assert_vast_xml().assert_ad_count(1)

    # Set up VPC to make a third request that is a match
    vpc.regenerate_automation_framework()

    # Add params that match the rule including case-insensitive comparison for content_genre
    vpc.content_title = "ace ventura: when nature calls"
    vpc.content_genre = "comedy"

    vast_result = VastValidator().test(vpc)

    # If there's one media in the vast we know our only aligned media passed targeting checks.
    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
@description(
    "Test that a media with custom url param targeting only filters requests that match the rule"
)
def test_media_targeting_custom_url_expression_same_key():
    case = Case("test_media_targeting_custom_url_expression_same_key")
    vpc = case.vpc
    vast_result = VastValidator().test(vpc)

    # The media should be filtered and not included in the vast
    vast_result.assert_vast_xml().assert_ad_count(0)
    vast_result.assert_filter(FilterReason.TARGETING_PARAMS)

    # Set up VPC to make a second request that is a match
    vpc.regenerate_automation_framework()
    vpc.add_custom_param("CP-5037_test", "anything")
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(1)

    # Set up VPC to make a third request that is not a match
    vpc.regenerate_automation_framework()
    vpc.add_custom_param("CP-5037_test", "invalid")
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(0)
    vast_result.assert_filter(FilterReason.TARGETING_PARAMS)

    # Set up VPC to make a fourth request that is not a match
    vpc.regenerate_automation_framework()
    vpc.add_custom_param("CP-5037_test", "bad")
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(0)
    vast_result.assert_filter(FilterReason.TARGETING_PARAMS)
