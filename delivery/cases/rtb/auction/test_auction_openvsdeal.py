import pytest
import logging

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator

BIDDER_PRICE_12 = "test_open_auction_beats_non_guaranteed_deal [2]"

BIDDER_PRICE_13 = "test_open_auction_beats_non_guaranteed_deal [1]"


@pytest.mark.regression
def test_open_auction_beats_non_guaranteed_deal():
    case = Case(
        "test_open_auction_beats_non_guaranteed_deal"
    )  # This is the file to test this case

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 2, "There should be two bidders for the auction"
    for bidder in bidders:
        # Validate auction types
        bid_requests = bidder.bid_requests
        assert (
            len(bid_requests) == 1
        ), "There should be one bid request from each bidder"
        bid_request = bid_requests[0]
        # Make sure the auction type is 1 - First Price Auction
        assert bid_request["at"] == 1, "Auction type should be 1 - First auction"
        # Validate Bid Responses
        bid_responses = bidder.bid_responses
        assert (
            len(bid_responses) == 1
        ), "There should be one Bid Response from each bidder"
        bid_response = bid_responses[0]
        # Validate Seat Bids in Bid Response
        seat_bids = bid_response.seat_bids
        assert len(seat_bids) == 1
        seat_bid = seat_bids[0]
        bids = seat_bid.bids
        assert len(bids) == 1
        bid = bids[0]
        if bidder.bidder_name == BIDDER_PRICE_12:
            assert float(bid.price) == 12.0, "Bid price should be 12.0"
        elif bidder.bidder_name == BIDDER_PRICE_13:
            assert float(bid.price) == 13.0, "Bid price should be 13.0"
            assert bid.deal_id == "", "Deal ID should be empty"
        else:
            assert False, "Unknown Bidder"

    # Validate winning bidder

    assert auction_validator.is_win_price_as_expected(
        13.0
    ), "Auction win price is wrong"
    assert auction_validator.is_applied_auction_type_as_expected(
        "FIRST_PRICE"
    ), "Auction type should be FIRST_PRICE"
    assert auction_validator.is_winning_deal_id_as_expected(
        ""
    ), "Winning Deal ID should be empty"


@pytest.mark.regression
@description(
    "A 20 High guaranteed deal will win against other guaranteed deal of 10 and high non-guaranteed of 25"
)
def test_high_guaranteed_deal_wins_over_other_guaranteed_and_other_deals():
    case = Case("test_high_guaranteed_deal_wins_over_other_guaranteed_and_other_deals")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()

    # alias of function for expected deal and price for rtb
    is_expected_deal_id = auction_validator.is_winning_deal_id_as_expected
    is_expected_price = auction_validator.is_win_price_as_expected

    # Validate winning bidder
    if not is_expected_price(20.0):
        logging.error("The expected win price is 20.0")
        assert False

    if not is_expected_deal_id("CP_3581_high_deal_win"):
        logging.error("The expected deal is CP_3581_high_deal_win")
        assert False


@pytest.mark.regression
@description("A 17 CPM High Open auction wins over non guaranteed deal with 16 CPM")
def test_high_open_auction_wins_over_non_guaranteed_deal():
    case = Case("test_high_open_auction_wins_over_non_guaranteed_deal")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()

    # alias of function for expected deal and price for rtb
    is_expected_deal_id = auction_validator.is_winning_deal_id_as_expected
    is_expected_price = auction_validator.is_win_price_as_expected

    # Validate winning bidder
    if not is_expected_price(17.0):
        logging.error("The expected win price is 17.0")
        assert False

    if not is_expected_deal_id(""):
        logging.error("The expected deal is to be empty")
        assert False


@pytest.mark.regression
def test_high_nonguranteed_deal_wins_over_othernonguranteed():
    case = Case("test_high_nonguranteed_deal_wins_over_othernonguranteed")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 2, "There should be 2 bidders for the auction"
    for bidder in bidders:
        # Validate auction types
        bid_requests = bidder.bid_requests
        assert (
            len(bid_requests) == 1
        ), "There should be one bid request from each bidder"
        bid_request = bid_requests[0]
        # Make sure the auction type is 1 - First Price Auction
        assert bid_request["at"] == 1, "Auction type should be 1 - First auction"
        # Validate Bid Responses
        bid_responses = bidder.bid_responses
        assert (
            len(bid_responses) == 1
        ), "There should be one Bid Response from each bidder"
        bid_response = bid_responses[0]
        # Validate Seat Bids in Bid Response
        seat_bids = bid_response.seat_bids
        assert len(seat_bids) == 1
        seat_bid = seat_bids[0]
        bids = seat_bid.bids
        assert len(bids) == 1
        bid = bids[0]
        if bid.deal_id.startswith("dnonguaranteedId"):
            assert float(bid.price) == 12.0, "Bid price should be 12.0"
        elif bid.deal_id.startswith("dnonguaranteed2"):
            assert float(bid.price) == 14.0, "Bid price should be 14.0"
        else:
            logging.error(
                f"The actual bidder has the deal [{bid.deal_id}] "
                f" is not in the expected deals [dnonguaranteedId,dnonguaranteed2]"
            )
            assert False, "Unknown Bidder"

    logging.info(auction_validator.winning_bidder_name)
    # Validate winning bidder
    assert auction_validator.is_win_price_as_expected(
        14.0
    ), "Auction win price is wrong"

    assert auction_validator.is_winning_deal_id_as_expected(
        "dnonguaranteed2"
    ), "Winning Deal ID should not be empty or different"


@pytest.mark.regression
def test_high_openbid_wins_over_otherlowOpenBids():
    case = Case("test_high_openbid_wins_over_otherlowOpenBids")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 3, "There should be 3 bidders for the auction"
    for bidder in bidders:
        # Validate auction types
        bid_requests = bidder.bid_requests
        assert (
            len(bid_requests) == 1
        ), "There should be one bid request from each bidder"
        bid_request = bid_requests[0]
        # Make sure the auction type is 1 - First Price Auction
        assert bid_request["at"] == 1, "Auction type should be 1 - First auction"
        # Validate Bid Responses
        bid_responses = bidder.bid_responses
        assert (
            len(bid_responses) == 1
        ), "There should be one Bid Response from each bidder"
        bid_response = bid_responses[0]
        # Validate Seat Bids in Bid Response
        seat_bids = bid_response.seat_bids
        assert len(seat_bids) == 1
        seat_bid = seat_bids[0]
        bids = seat_bid.bids
        assert len(bids) == 1
        bid = bids[0]
        bid_price = float(bid.price)
        if bid.deal_id == "":
            assert (
                bid_price == 13.0 or bid_price == 14.0 or bid_price == 15.0
            ), "Bid price should be 13.0 or 14.0 or 15.0"
        else:
            logging.error(
                f"The actual bidder has the deal [{bid.deal_id}] "
                f" is not in the expected deals [dnonguaranteedId,dnonguaranteed2]"
            )
            assert False, "Unknown Bidder"

    # Validate winning bidder

    assert auction_validator.is_win_price_as_expected(
        15.0
    ), "Auction win price is wrong"
    assert auction_validator.is_winning_deal_id_as_expected(
        ""
    ), "Winning Deal ID should be empty"
