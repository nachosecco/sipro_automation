import pytest
from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description


@pytest.mark.regression
@description(
    """
	This test case checks dealId and deal bid floor sent in bid request is sent back in response too.
	# Depends on one placement with configured floor of 1, an aligned media.
	"""
)
def test_dealid_param_sent_back_in_bid_response():
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("rtb-test-app")
        .private_auction(1)
        .deal_id("xzy-deal-id")
        .deal_bid_floor(2)
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
        .price_is(2.0)
        .deal_id_is("xzy-deal-id")
    )


@pytest.mark.regression
@description(
    """
	This test case no dealId sent in bid request is not set in in response too.
	# Depends on one placement with configured floor of 1, an aligned media.
	"""
)
def test_no_deal_id_param_no_deal_id_in_bid_response():
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
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
        .deal_id_is(None)
    )


@pytest.mark.regression
@description(
    """
	This test case checks dealId sent in bid request without bid floor in response we get bid floor as imp bid floor.
	# Depends on one placement with configured floor of 1, an aligned media.
	"""
)
def test_dealid_without_floor_param_sent_back_in_bid_response():
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("rtb-test-app")
        .private_auction(1)
        .deal_id("xzy-deal-id")
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
        .deal_id_is("xzy-deal-id")
    )
