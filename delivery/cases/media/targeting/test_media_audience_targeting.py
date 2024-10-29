import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason


@pytest.mark.smoke
def test_media_targeting_blocked_audience():
    case = Case("test_media_targeting_blocked_audience")
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assertTargeting().audience().assert_blocked()
    vast_result.assertFilter(FilterReason.TARGETING_AUDIENCE)
    vast_result.assertXML().assert_ad_count(0)


@pytest.mark.smoke
def test_media_targeting_allow_audience():
    case = Case("test_media_targeting_allow_audience")
    vpc = case.vpc

    vpc.did = "AUTO_DELIVERY_DID"

    vast_result = VastValidator().test(vpc)

    vast_result.assertTargeting().audience().assert_pass(expected_cpm="1.50")

    vast_result.assertXML().assert_ad_count(1)
