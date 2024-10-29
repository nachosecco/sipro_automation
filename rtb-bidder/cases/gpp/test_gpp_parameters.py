import pytest

from core.Description import description
from core.rtbRequestBuilder import RtbRequestBuilder


@description(
    """
    Test gpp and gpp_sid parameter are sent to delivery as any targeting is not allowed
    Placement has one media aligned and app name blacklist targeting is applied for app name "blocked_app_name"..
    """
)
@pytest.mark.regression
def test_gpp_parameter_with_targeting_ad_blocked():
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("other_than_blocked")
        .gpp(
            "DBABRg~BCAAAAA"
        )  #  targeted advertising OptOut notice is two and OptOut is zero
        .gpp_sid(9)  # section id - virginia
        .send()
    )

    rtb_response.is_empty()


@description(
    """
    Test gpp and gpp_sid parameter are sent to delivery as targeting is allowed
    Placement has one media aligned and app name blacklist targeting is applied for app name "blocked_app_name"..
    """
)
@pytest.mark.regression
def test_gpp_parameter_with_targeting_ad_allowed():
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("other-than-blocked")
        .gpp(
            "DBABRg~BAAAAAA"
        )  #  targeted advertising OptOut notice is zero and OptOut is zero
        .gpp_sid(9)  # section id - virginia
        .send()
    )

    (
        rtb_response.is_ok()
        .number_of_bids_is(1)
        .validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
        .ad_count_is(1)
    )


@description(
    """
	Test gpp and gpp_sid parameter are sent to delivery in regs ext object. Gpp value as any targeting is not allowed
	Placement has one media aligned and app name blacklist targeting is applied for app name "blocked_app_name"..
	"""
)
@pytest.mark.regression
def test_ext_gpp_parameter_with_targeting_ad_blocked():
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("other_than_blocked")
        .ext_gpp(
            "DBABRg~BCAAAAA"
        )  #  targeted advertising OptOut notice is two and OptOut is zero
        .ext_gpp_sid(9)  # section id - virginia
        .send()
    )
    rtb_response.is_empty()


@description(
    """
	Test gpp and gpp_sid parameter are sent to delivery in regs ext object. Gpp value as targeting is allowed
	Placement has one media aligned and app name blacklist targeting is applied for app name "blocked_app_name"..
	"""
)
@pytest.mark.regression
def test_ext_gpp_parameter_with_targeting_ad_allowed():
    rtb_response = (
        RtbRequestBuilder.mobile()  # Mobile (app) bid request type builder
        .bid_floor(1)
        .w(640)
        .h(480)
        .url("rtb-test-app.com")
        .bundle("rtb-test-app")
        .name("other-than-blocked")
        .ext_gpp(
            "DBABRg~BAAAAAA"
        )  #  targeted advertising OptOut notice is zero and OptOut is zero
        .ext_gpp_sid(9)  # section id - virginia
        .send()
    )

    (
        rtb_response.is_ok()
        .number_of_bids_is(1)
        .validate_vast()  # Request a vast validator, all calls from now on validates the vast xml
        .ad_count_is(1)
    )
