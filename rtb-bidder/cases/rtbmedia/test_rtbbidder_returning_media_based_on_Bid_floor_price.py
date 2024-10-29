import pytest

from core.Description import description
from core.rtbRequestBuilder import RtbRequestBuilder


@pytest.mark.regression
@description(
    """
	Validate rtbbidder is returning media when bidfloor is lower the media CPM.
	Any media will return only if the media CPM is higher the bid floor price
	Align a placement with 0 floor and media 10 dollors. Sending bid floor with 5 dollars , In response it should return the media
	"""
)
def test_rtbbidder_returning_media_when_floor_price_is_lower_then_media_cpm_manage_media():

    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .mobile()  # Mobile (app) bid request type builder
        .bid_floor(5)
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
        .price_is(5.5)
        .adomain_is([])
    )
