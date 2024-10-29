from core.Description import description
from core.rtbRequestBuilder import RtbRequestBuilder


@description(
    """
	This test will check the cat field in the bid response.
	"""
)
def test_cat_field():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("rtb-test-app")
        .send()
    )

    (
        rtb_response.is_ok()
        .number_of_bids_is(1)
        .validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
        .ad_count_is(1)
        .vast_version_is("4.0")
        .back()  # goes back to the bid_response validator, all calls from now on validates the bid response again
        .matches_request_transaction_id()
        .price_is(1.0)
        .cat_is(["IAB-1"])
    )
