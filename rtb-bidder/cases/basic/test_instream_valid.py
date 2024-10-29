import pytest
from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description


@description(
    """
    This test case is to validate that if all the required parameters are passed in instream bid request then it should return
    200 status code with valid media.
    """
)
@pytest.mark.regression
def test_instream_valid():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .web()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .url("siprocal.com")
        .ref("rtb-test")
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
        .adomain_is(["https://www.smaato.com"])
    )
