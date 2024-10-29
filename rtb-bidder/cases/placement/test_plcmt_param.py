import pytest
from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description


@description(
	"""
	Test plcmt parameter valued as 2 is sent to delivery.
	"""
)
@pytest.mark.regression
def test_send_plcmt_parameter_from_bidder_service():
	rtb_response = (
		RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
			.bid_floor(1)
			.w(640)
			.h(480)
			.url("rtb-test-app.com")
			.bundle("rtb-test-app")
			.name("rtb-test-app")
			.plcmt(2)
			.send()
	)

	(
		rtb_response.is_ok()
			.number_of_bids_is(1)
			.validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
			.ad_count_is(1)
	)