import pytest
from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description
import uuid


@description(
    """
	This test case is to validate that if mandatory field site.page is passed as blank in instream bidrequest then error is thrown.
	It should throw 400 bad request
	It should throw error message "uid parameter or site.id is mandatory."
	"""
)
@pytest.mark.regression
def test_empty_site_id_for_instream():
	rtb_response = (
		RtbRequestBuilder
		# Automatically assigns the placement uid
		.web("")
		.bid_floor(1)
		.ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
		.url("siprocal.com")
		.ref("rtb-test-ref")
		.send()
	)
	(rtb_response.is_bad_request().has_error_message("uid parameter or site.id is mandatory"))
