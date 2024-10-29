import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


# Test Auction has no winner when placement floor price is grater than bid price
@pytest.mark.regression
@description(
    """Verifying there isn't any winner when the placement floor price is grater than bid price
        Placement floor price = $7
        DSP outgoing programmatic bidder price= &5
        Result: validation auction has no final winner """
)
def test_bidder_loose_over_high_placement_floor_price_against_bid_floor_pric():
    case = Case(
        "test_bidder_loose_over_high_placement_floor_price_against_bid_floor_pric"
    )

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # this test cases has 1 programmatic demand and should not be returned in the vast
    vast_result.assert_vast_xml().assert_ad_count(0)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 1, "There should be one bidders for the auction"
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
        assert float(bid.price) == 5.0, "Bid price should be 5.0"
        # validation auction has no final winner
        vast_result.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
@description(
    """Verifying there is a winner when the placement floor price is less than bid price
        Placement floor price = $7
        DSP outgoing programmatic bidder price= &10
        Result: validation auction has a winner """
)
def test_bidder_win_over_high_bid_floor_price_against_lower_placement_floor_price():
    case = Case(
        "test_bidder_win_over_high_bid_floor_price_against_lower_placement_floor_price"
    )

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # this test cases has 1 programmatic demand and should be returned in the vast
    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 1, "There should be one bidders for the auction"
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
        assert float(bid.price) == 10.0, "Bid price should be 10.0"
        # validation auction Final winner price
        assert auction_validator.is_win_price_as_expected(10.0)


@pytest.mark.regression
@description(
    """Verifying there isn't any winner when the DSP outgoing bid request is less than incoming bid request
        Placement with $7 floor price
        DSP outgoing bid request $5
        Incoming bid request MIN PRICE $6
        AND DYNAMIC PRICE =TRUE and BID MERGIN 10% """
)
def test_rtb_service_bidder_loose_over_lower_incoming_rtb_floor_price_against_lower_dsp_outgoing_floor_price():
    case = Case(
        "test_rtb_service_bidder_loose_over_lower_incoming_rtb_floor_price_against_lower_dsp_outgoing_floor_price"
    )

    vpc = case.vpc
    vpc.min_price = "6"
    vpc.use_dynamic_pricing = "true"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # this test cases has 1 programmatic demand and should be returned in the vast
    vast_result.assert_vast_xml().assert_ad_count(0)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 1, "There should be one bidders for the auction"
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
        assert float(bid.price) == 5.0, "Bid price should be 5.0"
        # validation auction has no final winner
        vast_result.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
@description(
    """Verifying there is a winner when the DSP outgoing bid request is grater than incoming bid request
        Placement with $7 floor price
        DSP outgoing bid request $5
        Incoming bid request MIN PRICE $3
        AND DYNAMIC PRICE =TRUE and BID Margin 10% """
)
def test_rtb_service_bidder_win_over_lower_incoming_min_price_against_higher_outgoing_bid_price():
    case = Case(
        "test_rtb_service_bidder_win_over_lower_incoming_min_price_against_higher_outgoing_bid_price"
    )

    vpc = case.vpc
    vpc.min_price = "3"
    vpc.use_dynamic_pricing = "true"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # this test cases has 1 programmatic demand and should be returned in the vast
    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 1, "There should be one bidders for the auction"
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
        assert float(bid.price) == 5.0, "Bid price should be 5.0"
        # validation auction Final winner price
        assert auction_validator.is_win_price_as_expected(5.0)
