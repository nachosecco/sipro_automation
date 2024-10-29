from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description


@description(
    """
	Given an nonexistent placement uid

	Bidder should return:
	- statusCode:404
	- error: Not Found
	- matching transaction id
	- matching placement id
	"""
)
def test_nonexistent_placement_should_return_not_found():
    # This line is here to investigate if we can link cases with its data by referencing the test method
    # logging.info(f"Current test is: {test_nonexistent_placement_should_return_not_found.__name__}")
    rtb_response = (
        RtbRequestBuilder.mobile("NON_EXISTENT_PLACEMENT_UID")
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .bid_floor(10)
        .name("rtb-test-app")
        .send()
    )
    (
        rtb_response.is_not_found()
        .has_error_message("Not Found")
        .matches_request_transaction_id()
        .placement_uid_is("NON_EXISTENT_PLACEMENT_UID")
    )
