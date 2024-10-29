import pytest
from core.rtbRequestBuilder import RtbRequestBuilder
from core.Description import description


@description(
	"""
	This test case checks if a media is aligned with advertiser domain and that advertiser domain is passed as
	badv in rtb request then media will get filtered
	"""
)
@pytest.mark.regression
def test_media_filter_if_advertiser_domain_is_blockeddomain():
	rtb_response = (RtbRequestBuilder
					# Automatically assigns the placement uid
					.mobile()  # Mobile (app) bid request type builder
			.bid_floor(1)
					.ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
					.url("rtb-test-app.com")
					.bundle("rtb-test-app")
					.name("rtb-test-app")
					.badv(["ford.com"])
					.send())

	(rtb_response
	 .is_empty())


@description(
		"""
		This test case checks if a media is aligned with advertiser domain and that advertiser domain is different than the addomain passed as
		badv in rtb request then media will not get filtered
		"""
)
@pytest.mark.regression
def test_not_media_filter_if_advertiser_domain_is_not_blockeddomain():
	rtb_response = (RtbRequestBuilder
					# Automatically assigns the placement uid
					.mobile()  # Mobile (app) bid request type builder
					.bid_floor(1)
					.ifa("71299b6e-a1d8-4b20-bbfd-b271d9bbe5df")
					.url("rtb-test-app.com")
					.bundle("rtb-test-app")
					.name("rtb-test-app")
					.badv(["ford.com"])
					.send())

	(rtb_response
	 .is_ok()
	 .number_of_bids_is(1)
	 .validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
	 .ad_count_is(1)
	 .vast_version_is("4.0")
	 .back()  # goes back to the bid_response validator, all calls from now on validates the bid response again
	 .matches_request_transaction_id()
	 .price_is(1.0)
	 .adomain_is(["chevrolet.com"]))