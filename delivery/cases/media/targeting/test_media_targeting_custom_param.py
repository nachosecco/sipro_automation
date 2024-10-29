import pytest

from core.Description import description
from core.case import Case
from core.enums.filterReason import FilterReason
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    """In a scenario with a media with custom param,
it will test that when the value is in the request the media targeting will not be blocked"""
)
def test_media_targeting_custom_param_allow():
    case = Case("test_media_targeting_custom_param_allow")

    vpc = case.vpc
    vpc.add_custom_param(
        "test_media_targeting_custom_param_allow",
        "allow",
    )

    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_ad_count(1)

    # We are going to test again, but now with upper case in the value of the custom param
    vpc.regenerate_automation_framework()
    vpc.add_custom_param(
        "test_media_targeting_custom_param_allow",
        "ALLOW",
    )
    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_ad_count(1)


@description(
    """In a scenario with a media with custom param,
    it will test that when the value is in the request the media targeting will be blocked
    and have the filter reason TARGETING_PARAMS"""
)
def test_media_targeting_custom_param_block():
    case = Case("test_media_targeting_custom_param_block")

    vpc = case.vpc
    vpc.add_custom_param(
        "test_media_targeting_custom_param_allow",
        "block",
    )

    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_ad_count(0)

    vast_result.assertFilter(FilterReason.TARGETING_PARAMS)
