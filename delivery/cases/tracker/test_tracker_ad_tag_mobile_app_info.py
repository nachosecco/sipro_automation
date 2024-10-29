import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_tracker_ad_tag_mobile_info_valid_values():
    case = Case("test_tracker_ad_tag_mobile_info_valid_values")
    vpc = case.vpc
    vpc.app_id = "app_id"
    vpc.app_name = "app_name"
    vpc.app_ver = "3.0"
    vpc.app_uri = "https://www.app_uri.com"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("app_name", vpc.app_name)
    assertTrackerTags.ad_tag("app_id", vpc.app_id)
    assertTrackerTags.ad_tag("app_uri", vpc.app_uri)
    assertTrackerTags.ad_tag("app_ver", vpc.app_ver)


@pytest.mark.regression
def test_tracker_ad_tag_mobile_info_empty_values():
    case = Case("test_tracker_ad_tag_mobile_info_empty_values")
    vpc = case.vpc
    vpc.app_id = "app_id"
    vpc.app_name = ""
    vpc.app_ver = ""
    vpc.app_uri = ""
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("app_name", vpc.app_name)
    assertTrackerTags.ad_tag("app_id", vpc.app_id)
    assertTrackerTags.ad_tag("app_uri", vpc.app_uri)
    assertTrackerTags.ad_tag("app_ver", vpc.app_ver)
