import pytest
from core.case import Case
from core.Description import description
from core.dto.event import EventType
from core.vastValidator import VastValidator


@pytest.mark.regression
@description("scenario to check dynamic pricing for managed and rtb demand")
def test_dynamic_pricing_ok():
    case = Case("test_dynamic_pricing_ok")

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "10"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)

    # this test cases has 3 ads
    vast_result.assert_vast_xml().assert_ad_count(3)

    # Based that bidder_margin=20% and min_price=10.0 and close_price = 12
    # ((($12-$10) * 0.2) +$10) = $10.4
    rtb_price = 10.4

    # Based that bidder_margin=20% and min_price=10.0 and media cpm = 20
    # (($20-$10) * 0.2) +$10) = $12.0
    media_managed = 12.0

    # Based that bidder_margin=20% and min_price=10.0 and media cpm = 20
    # (($20-$10) * 0.2) +$10) = $12.0
    media_managed_2 = 12.0

    vast_result.assert_extension().assert_price_are(
        [media_managed, media_managed_2, rtb_price]
    )


@pytest.mark.regression
@description(
    "scenario to check dynamic pricing for placement floor in opportunity event is equal to min_price"
)
def test_dynamic_pricing_with_check_opportunity_event():
    case = Case("test_dynamic_pricing_with_check_opportunity_event")

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "15"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.VIDEOTRUEFIRSTCALL
    event.beacon_event_type = EventType.VIDEOTRUEFIRSTCALL.name
    event.floor = "15.0"

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)


@pytest.mark.regression
@description("scenario to check dynamic pricing for managed with margin is 0")
def test_dynamic_pricing_managed_margin0():
    case = Case("test_dynamic_pricing_managed_margin0")

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "5"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    # Based that bidder_margin=20% and min_price=5.0 and media cpm = 10
    # ((10-$5) * 0.0) +$5) = $5.0
    media_managed = 5.0

    vast_result.assert_extension().assert_price_are([media_managed])


@pytest.mark.regression
@description("scenario to check dynamic pricing for rtb with margin is 0")
def test_dynamic_pricing_rtb_margin0():
    case = Case("test_dynamic_pricing_rtb_margin0")

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "5"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    # Based that bidder_margin=20% and min_price=5.0 and media cpm = 10
    # ((10-$5) * 0.0) +$5) = $5.0
    media_rtb = 5.0

    vast_result.assert_extension().assert_price_are([media_rtb])
