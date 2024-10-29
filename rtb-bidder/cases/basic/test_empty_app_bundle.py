import pytest
from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description

@pytest.mark.regression
@description(
	"""
	This test case is to validate that if app.bundle is not passed in bidrequest then error is thrown.
	It should throw 400 bad request
	"""
)

def test_empty_app_bundle():
	rtb_response = (
		RtbRequestBuilder
		# Automatically assigns the placement uid
		.mobile("test")  # Mobile (app) bid request type builder
		.bid_floor(1)
		.ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
		.url("rtb-test-app.com")
		.bundle("")
		.name("rtb-test-app")
		.send()
	)

	(rtb_response
	 .is_bad_request()
	 .has_error_message("Invalid request content.")
	 )
