import pytest

from core.Description import description
from core.case import Case
from core.enums.filterReason import FilterReason
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "dynamic pricing for a managed media house ad is not blocked by filter reason"
)
def test_dynamic_with_media_house_ad_always_ok():
    case = Case("test_dynamic_with_media_house_ad_always_ok")

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "0"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # this test cases has 1 ad
    vast_result.assert_vast_xml().assert_ad_count(1)

    # Based that bidder_margin=20% and min_price=0.0 and media cpm = 0
    # ((0-0) * 0.2) + 0) = 0
    house_ad_media = 0.0

    vast_result.assert_extension().assert_price_are([house_ad_media])


@pytest.mark.regression
@description(
    "dynamic pricing for a managed media with cpm 20 and min price 30 it should be blocked"
)
def test_dynamic_with_when_min_price_is_above_cpm_of_managed_media_then_media_is_blocked():
    case = Case(
        "test_dynamic_with_when_min_price_is_above_cpm_of_managed_media_then_media_is_blocked"
    )

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "30"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # this test cases has 0 ad
    vast_result.assert_vast_xml().assert_ad_count(0)

    vast_result.assertFilter(FilterReason.BLOCKED_CPM_BELOW_MIN_PRICE)


@pytest.mark.regression
@description(
    "dynamic pricing for a programmatic with deal with deal_floor 5 and min price 10 it should be blocked"
)
def test_dynamic_with_programmatic_with_deal_media_is_blocked_by_filter():
    case = Case("test_dynamic_with_programmatic_with_deal_media_is_blocked_by_filter")

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "15"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # this test cases has 0 ad
    vast_result.assert_vast_xml().assert_ad_count(0)


# comminting out  as of now . this log will only work with granrtee deal
# vast_result.assertLogsDelivery("blocked by Price below min price")
