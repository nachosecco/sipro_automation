import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "In a placement that aligned open auction, then bid that responded with deal id, should be accepted and win"
)
def test_rtb_auction_open_auction_deal_not_requested_wins():
    case = Case("test_rtb_auction_open_auction_deal_not_requested_wins")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
@description(
    "In a placement that aligned with 2 open auction, then bid that responded with deal id, should be accepted and wins"
)
def test_rtb_auction_2_open_auction_then_bid_with_deal_not_requested_wins():
    case = Case("test_rtb_auction_2_open_auction_then_bid_with_deal_not_requested_wins")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()

    assert auction_validator.is_win_price_as_expected(80.0)


@pytest.mark.regression
@description(
    "In a first price placement that aligned with a first price open deal, and 2 bidders,"
    " then bid that responded with deal id not requested, should be accepted and wins"
    " requested deal bid price is 50"
    " not requested deal bid price is 80, it should win, because of higher bid price"
)
def test_rtb_auction_first_price_placement_with_first_price_open_deal_with_not_requested_deal_should_win():
    case = Case(
        "test_rtb_auction_first_price_placement_with_first_price_open_deal_with_not_requested_deal_should_win"
    )
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()
    assert auction_validator.is_win_price_as_expected(80.0)


@pytest.mark.regression
@description(
    "In a placement first price that aligned with open deal first price and open line, with 2 bidders,"
    " then bid that responded with deal id not requested, should be accepted and loss"
    " requested deal bid price is 60, it should win, because higher bid price"
    " not requested deal bid price is 20, it should loss"
)
def test_rtb_auction_first_price_placement_with_first_price_open_deal_with_not_requested_deal_should_loss():
    case = Case(
        "test_rtb_auction_first_price_placement_with_first_price_open_deal_with_not_requested_deal_should_loss"
    )
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()
    assert auction_validator.is_win_price_as_expected(60.0)


@pytest.mark.regression
@description(
    "In a placement first price that aligned with private deal first price with 1 bidders,"
    " then bid that responded with deal id not requested, should be not be accepted and loss"
)
def test_rtb_auction_first_price_placement_with_first_price_private_deal_with_not_requested_deal_should_loss():
    case = Case(
        "test_rtb_auction_first_price_placement_with_first_price_private_deal_with_not_requested_deal_should_loss"
    )
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
@description(
    "In a placement that aligned open auction and multiple impressions,"
    " then bidder with multiple impressions "
    " that responded with 2 bids with a deal id not requested, should be accepted and wins both"
)
def test_rtb_auction_open_auction_with_multiple_impression_with_deal_not_requested_should_have_2wins():
    case = Case(
        "test_rtb_auction_open_auction_with_multiple_impression_with_deal_not_requested_should_have_2wins"
    )
    vpc = case.vpc
    vpc.pod_size = "2"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(2)


@pytest.mark.regression
@description(
    "In a placement that aligned open deal , then bid that responded with deal id null, should be accepted and win"
)
def test_rtb_auction_open_auction_deal_null_not_requested_wins():
    case = Case("test_rtb_auction_open_auction_deal_null_not_requested_wins")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)
