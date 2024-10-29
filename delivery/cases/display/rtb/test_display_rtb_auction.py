import pytest
from core.case import Case
from core.validator.DisplayPlacementValidator import DisplayPlacementValidator


@pytest.mark.regression
def test_display_placement_rtb_auction_26():
    case = Case("test_display_placement_rtb_auction_26")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)
    bid_request_validator = dpl_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_display_placement_rtb_auction_26"
    )

    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    auction_validator = dpl_result.validate_rtb_auction()
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

        # # Validate winning bidder
    assert auction_validator.is_winning_bidder_name_as_expected(
        "test_display_placement_rtb_auction_26"
    ), "Auction winning bidder name is wrong"
    assert auction_validator.is_win_price_as_expected(
        12.0
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


@pytest.mark.regression
def test_display_placement_rtb_auction_25():
    case = Case("test_display_placement_rtb_auction_25")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)
    bid_request_validator = dpl_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_display_placement_rtb_auction_25"
    )

    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    auction_validator = dpl_result.validate_rtb_auction()
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

        # # Validate winning bidder
    assert auction_validator.is_winning_bidder_name_as_expected(
        "test_display_placement_rtb_auction_25"
    ), "Auction winning bidder name is wrong"
    assert auction_validator.is_win_price_as_expected(
        12.0
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


@pytest.mark.regression
def test_display_placement_rtb_auction_24():
    case = Case("test_display_placement_rtb_auction_24")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)
    bid_request_validator = dpl_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_display_placement_rtb_auction_24"
    )

    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    auction_validator = dpl_result.validate_rtb_auction()
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

        # # Validate winning bidder
    assert auction_validator.is_winning_bidder_name_as_expected(
        "test_display_placement_rtb_auction_24"
    ), "Auction winning bidder name is wrong"
    assert auction_validator.is_win_price_as_expected(
        12.0
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


@pytest.mark.regression
def test_display_placement_rtb_auction_23():
    case = Case("test_display_placement_rtb_auction_23")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)
    bid_request_validator = dpl_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_display_placement_rtb_auction_23"
    )

    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    auction_validator = dpl_result.validate_rtb_auction()
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

        # # Validate winning bidder
    assert auction_validator.is_winning_bidder_name_as_expected(
        "test_display_placement_rtb_auction_23"
    ), "Auction winning bidder name is wrong"
    assert auction_validator.is_win_price_as_expected(
        12.0
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


@pytest.mark.regression
def test_display_placement_rtb_auction_22():
    case = Case("test_display_placement_rtb_auction_22")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)
    bid_request_validator = dpl_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_display_placement_rtb_auction_22"
    )

    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    auction_validator = dpl_result.validate_rtb_auction()
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

        # # Validate winning bidder
    assert auction_validator.is_winning_bidder_name_as_expected(
        "test_display_placement_rtb_auction_22"
    ), "Auction winning bidder name is wrong"
    assert auction_validator.is_win_price_as_expected(
        12.0
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
