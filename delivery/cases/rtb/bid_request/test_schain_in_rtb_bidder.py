import logging

import pytest
from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    """
	Create a Placement with one programmatic demand aligned
	verify that the bid_request returns siprocal.com in schain domain
	Expected result
	"asi": "siprocalads.com"
	"""
)
def test_schain_in_rtb_bidder():
    domain = "siprocalads.com"
    case = Case("test_schain_in_rtb_bidder")
    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bid_request_validator.is_rtb_version_as_expected(2.6)
        if len(bidder.bid_requests) == 0:
            logging.error("There was no request for the bidder")
            assert False
        for bid_request in bidder.bid_requests:
            assert (
                bid_request["source"]["ext"]["schain"].get("domain") is None
            ), "asi expected to be siprocalads.com but didn't matched"
