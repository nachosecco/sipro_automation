import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description(
	"Will check that a bidder with with duplicated data of method content"
	" are not duplicated in the request sent to to the bidder"
)

@pytest.mark.regression
def test_bid_request_video_delivery_method_not_duplicated():
	case = Case("test_bid_request_video_delivery_method_not_duplicated")

	vpc = case.vpc

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assertCase(case)

	vast_result.assert_vast_xml().assert_ad_count(1)

	auction_validator = vast_result.validate_rtb_auction()

	bidders = auction_validator.bidders
	bid_request = bidders[0].bid_requests

	imp_request = bid_request[0].get("imp")[0]
	video_request = imp_request.get("video", None)
	assert (
			video_request is not None
	), "we are expecting that there is a video object in impression object"

	delivery_method_request = video_request.get("delivery", None)
	assert (
			delivery_method_request is not None
	), "we are expecting that there is a delivery object in video object"

	delivery_method_request.sort()

	assert delivery_method_request == [
		1,
		2,
		3,
	], "we are expecting that there is a delivery object containing only 1,2,3"

@pytest.mark.regression
def test_bid_request_video_delivery_method_not_duplicated_with_bidder_has_more_values():
	case = Case("test_bid_request_video_delivery_method_not_duplicated_with_bidder_has_more_values")

	vpc = case.vpc

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assertCase(case)

	vast_result.assert_vast_xml().assert_ad_count(1)

	auction_validator = vast_result.validate_rtb_auction()

	bidders = auction_validator.bidders
	bid_request = bidders[0].bid_requests

	imp_request = bid_request[0].get("imp")[0]
	video_request = imp_request.get("video", None)
	assert (
			video_request is not None
	), "we are expecting that there is a video object in impression object"

	delivery_method_request = video_request.get("delivery", None)
	assert (
			delivery_method_request is not None
	), "we are expecting that there is a delivery object in video object"

	delivery_method_request.sort()

	assert delivery_method_request == [
		1,
		2,
		3,
	], "we are expecting that there is a delivery object containing only 1,2,3"
