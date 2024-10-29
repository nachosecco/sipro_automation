import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator
from core.dto.event import EventType, Event


@pytest.mark.regression
@description("Auction deal win against low CPM placement floor.")
def test_auction_valid_bid_win_on_low_placement_floor():
    case = Case("test_auction_valid_bid_win_on_low_placement_floor")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()

    assert auction_validator.is_winning_deal_id_as_expected(
        "CP_3583"
    ), "Expected Deal didn't WiN the Auction . Expected Deal is CP_3583"
    assert auction_validator.is_win_price_as_expected(
        10.0
    ), "Deal Win Price is Wrong ,Expected Deal win price is 10.0"


@pytest.mark.regression
@description("Auction deal lose against high CPM placement floor.")
def test_auction_invalid_bid_lose_on_high_placement_floor():
    case = Case("test_auction_invalid_bid_lose_on_high_placement_floor")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(0)

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.bidLossReasonCode = "LOST_TO_HIGHER_BID"
    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)


@pytest.mark.regression
@description(
    "2nd price Auction deal loses against higher CPM placement floor when final winning price is low"
)
def test_auction_second_price_bid_lose_on_high_placement_floor():
    case = Case("test_auction_second_price_bid_lose_on_high_placement_floor")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(0)

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.result = "NOBID"
    event.bidLossReasonCode = "LOST_TO_HIGHER_BID"
    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)


@pytest.mark.regression
@description(
    "Auction open exchange loses against higher CPM placement auction increment floor"
    "conf:"
    "floor = 1"
    "auction increment floor = 100"
    "bid price = 10.05"
)
def test_auction_open_exchange_bid_lose_on_high_placement_auction_increment_floor():
    case = Case(
        "test_auction_open_exchange_bid_lose_on_high_placement_auction_increment_floor"
    )
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(0)

    event = Event()
    event.event_type = EventType.RTB_EVENT

    event.lossReasonCode = "BID_WAS_BELOW_AUCTION_FLOOR"

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)


@pytest.mark.regression
@description(
    "Auction with deal win when higher CPM placement auction floor, because is auction increment floor is not used"
    "conf:"
    "floor = 1"
    "auction increment floor = 100"
    "bid price = 20.0"
)
def test_auction_with_deal_bid_win_on_high_placement_auction_increment_floor():
    case = Case(
        "test_auction_with_deal_bid_win_on_high_placement_auction_increment_floor"
    )
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)
