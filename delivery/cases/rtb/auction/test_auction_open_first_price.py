import logging

import pytest

from core.case import Case
from core.vastValidator import VastValidator

BIDDER_PRICE_10 = "test_auction_open_first_price [2]"

BIDDER_PRICE_20 = "test_auction_open_first_price"


# Test First Price Open Auction
@pytest.mark.regression
def test_auction_open_first_price():
    case = Case("test_auction_open_first_price")  # This is the file to test this case

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

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
        if len(bid_responses) < 1:
            logging.error("The are none bid responses ")
        assert (
            len(bid_responses) == 1
        ), "There should be one Bid Response from each bidder"
        bid_response = bid_responses[0]
        # Make sure currency property in Bid Responses are set to USD
        assert bid_response.currency == "USD", "Currency in Bid Response should be USD"
        # Validate Seat Bids in Bid Response
        seat_bids = bid_response.seat_bids
        assert len(seat_bids) == 1
        seat_bid = seat_bids[0]
        assert int(seat_bid.group) == 0
        assert seat_bid.seat == ""
        bids = seat_bid.bids
        assert len(bids) == 1
        bid = bids[0]
        if bid.win_notice_url == "http://www.winnerurl.com/price10":
            assert float(bid.price) == 10.0, "Bid price should be 10.0"

            assert (
                bid.loss_notice_url == "http://www.looseurl.com/price10"
            ), "Auction Loss Notice URL is wrong"
            assert bid.deal_id == "", "Deal ID should be empty"

        elif bid.win_notice_url == "http://www.winnerurl.com/price20":
            assert float(bid.price) == 20.0, "Bid price should be 20.0"

            assert (
                bid.loss_notice_url == "http://www.looseurl.com/price20"
            ), "Auction Loss Notice URL is wrong"
            assert bid.deal_id == "", "Deal ID should be empty"

        else:
            assert False, "Unknown Bidder"

    # Validate Win and Loss Notice URLs
    assert auction_validator.is_win_notice_url_as_expected(
        "http://www.winnerurl.com/price20"
    ), "Auction Win Notice URL is wrong"
    assert (
        len(auction_validator.loss_notice_urls) == 1
    ), "There should be only one Auction Loss Notice"
    assert (
        auction_validator.loss_notice_urls[0] == "http://www.looseurl.com/price10"
    ), "Auction Loss Notice URL is wrong"

    # Validate winning bidder
    assert auction_validator.is_win_price_as_expected(
        20.0
    ), "Auction win price is wrong"
    assert auction_validator.is_applied_auction_type_as_expected(
        "FIRST_PRICE"
    ), "Auction type should be FIRST_PRICE"
    assert auction_validator.is_winning_deal_id_as_expected(
        ""
    ), "Winning Deal ID should be empty"
    assert auction_validator.is_winning_seat_id_as_expected(
        ""
    ), "Winning Seat ID should be empty"
