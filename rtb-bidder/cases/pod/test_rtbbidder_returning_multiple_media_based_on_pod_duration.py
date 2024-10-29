import pytest

from core.Description import description
from core.rtbRequestBuilder import RtbRequestBuilder


@pytest.mark.regression
@description(
    """
	Validate rtbbidder is returning multiple media when pod duration is non-empty or non zero.
	Number of media will depend on duration of pod.
	Align a placement with 5 bid floor and 3 medias each of 30second. Send pod duration as 90 seconds , In response it should
	return all 3 medias objects
	"""
)
def test_rtbbidder_returning_multiple_media_based_on_pod_duration():
    rtb_response = (
        RtbRequestBuilder
        # Automatically assigns the placement uid
        .mobile()  # Mobile (app) bid request type builder
        .bid_floor(5)
        .ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("rtb-test-app")
        .max_duration(30)
        .max_seq(3)
        .pod_dur(90)
        .send()
    )

    (
        rtb_response.is_ok()
        .number_of_bids_is(1)
        .number_of_bidobjects_is(3)
        .validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
        .vast_version_is("4.0")
        .back()  # goes back to the bid_response validator, all calls from now on validates the bid response again
        .matches_request_transaction_id()
    )
