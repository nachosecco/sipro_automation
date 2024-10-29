import pytest
from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description


@description(
    """
	This test case is to validate that if mandatory field site.page is passed as blank in instream bidrequest then error is thrown.
	It should throw 400 bad request
	It should throw error message "Invalid request content."
	"""
)
@pytest.mark.regression
def test_empty_page():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .web("test")  # Mobile (app) bid request type builder
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .url("")
        .ref("rtb-test-ref")
        .send()
    )

    (rtb_response.is_bad_request().has_error_message("Invalid request content."))


@description(
    """
	This test case is to validate that if mandatory field site.ref is passed as blank in instream bidrequest then error is thrown.
	It should throw 400 bad request
	It should throw error message "Invalid request content."
	"""
)
@pytest.mark.regression
def test_empty_ref():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .web("test")  # Mobile (app) bid request type builder
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .url("test.com")
        .ref("")
        .send()
    )

    (rtb_response.is_bad_request().has_error_message("Invalid request content."))
