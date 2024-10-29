import pytest
from core.case import Case
from core.vastValidator import VastValidator


# Test Bid Request ID
@pytest.mark.regression
def test_bid_request_id():
    case = Case("test_bid_request_id")  # Reusing Auction test data to test this case

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    assert len(bidders) == 2, "There should be two bidders"
    bid_request_ids = []
    for bidder in bidders:
        bid_requests = bidder.bid_requests
        assert (
            len(bid_requests) == 1
        ), "There should be one bid request from each bidder"
        bid_request = bid_requests[0]
        bid_request_ids.append(bid_request["id"])
    assert len(bid_request_ids) == 2, "There should be two Bid Request IDs"
    assert bid_request_ids[0] != bid_request_ids[1], "Bid Request ID should be unique"
