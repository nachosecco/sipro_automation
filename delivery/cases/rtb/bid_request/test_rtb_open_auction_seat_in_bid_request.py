import logging

import pytest

from core.case import Case
from core.vastValidator import VastValidator

W_SEATS_DEFAULT = ["Seat1", "anotherSeat"]
B_SEATS_DEFAULT = ["Seat2"]


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_2():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_2")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, "Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_2 [1]",
                ["seat1"],
                ["seat2"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_3():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_3")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_3 [1]",
                ["seat1"],
                ["seat2"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_4():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_4")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_4 [1]",
                ["seat1"],
                ["seat2"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_5():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_5")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, "Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_5 [2]",
                ["Seat1"],
                ["seat2"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_6():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_6")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_6 [1]",
                ["seat1"],
                ["seat2"],
            )


def test_open_auction_seat_in_bid_request_rtb_2_6_with_2seats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_6_with_2seats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_6_with_2seats [2]",
                ["seat1", "anotherSeat"],
                ["seat2"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_5_with_2seats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_5_with_2seats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_5_with_2seats [1]",
                ["seat1", "anotherSeat"],
                ["seat2"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_4_with_2seats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_4_with_2seats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_4_with_2seats [1]",
                ["seat1", "anotherSeat"],
                ["seat2"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_3_with_2seats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_3_with_2seats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_3_with_2seats [1]",
                ["seat1", "anotherSeat"],
                ["seat2"],
            )


def assert_seats(
    bid_request,
    bidder_name,
    expected_w_bidder_name,
    expected_w_seats=None,
    expected_b_seat=None,
):
    if bidder_name == expected_w_bidder_name:
        if expected_w_seats is None:
            expected_w_seats = W_SEATS_DEFAULT
        assert_seat(bid_request, "wseat", expected_w_seats, "WSeat", bidder_name)

    else:
        if expected_b_seat is None:
            expected_b_seat = B_SEATS_DEFAULT
        assert_seat(bid_request, "bseat", expected_b_seat, "BSeat", bidder_name)


def assert_seat(bid_request, field_name, expected_seats, type_seat, bidder_name):
    actual_seats = bid_request.get(field_name, [])
    found_w_seat = find_seats_in_request(expected_seats, actual_seats)
    equals = len(found_w_seat) == len(expected_seats)
    if not equals:
        logging.error(
            f"In Bidder Name [{bidder_name}] \nfor type seat {type_seat} we are expecting seats {expected_seats}] "
            f"and we got [{actual_seats}]"
        )
    assert equals


def find_seats_in_request(expected_seats, actual_seats):
    found_w_seat = []
    for expected_seat in expected_seats:
        for actual_seat in actual_seats:
            if actual_seat == expected_seat:
                found_w_seat.append(actual_seat)
    return found_w_seat


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_2_with_2seats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_2_with_2seats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_2_with_2seats [1]",
                ["seat1", "anotherSeat"],
                ["seat2"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_2_with_2Bseats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_2_with_2Bseats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name

        for bid_request in bidder.bid_requests:
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_2_with_2Bseats [2]",
                ["seat1"],
                ["bseat1", "bAnotherSeat"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_3_with_2Bseats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_3_with_2Bseats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_3_with_2Bseats [2]",
                ["seat1"],
                ["bseat1", "bAnotherSeat"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_4_with_2Bseats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_4_with_2Bseats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_4_with_2Bseats [2]",
                ["seat1"],
                ["bseat1", "bAnotherSeat"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_5_with_2Bseats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_5_with_2Bseats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_5_with_2Bseats [2]",
                ["Seat1"],
                ["bseat1", "bAnotherSeat"],
            )


@pytest.mark.regression
def test_open_auction_seat_in_bid_request_rtb_2_6_with_2Bseats():
    case = Case("test_open_auction_seat_in_bid_request_rtb_2_6_with_2Bseats")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bidder_name = bidder.bidder_name
        for bid_request in bidder.bid_requests:
            assert_seats(
                bid_request,
                bidder_name,
                "test_open_auction_seat_in_bid_request_rtb_2_6_with_2Bseats [1]",
                ["seat1"],
                ["bseat1", "bAnotherSeat"],
            )
