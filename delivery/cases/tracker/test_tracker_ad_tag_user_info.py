import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_tracker_ad_tag_user_info_valid_values_IDFA():
    case = Case("test_tracker_ad_tag_user_info_valid_values_IDFA")
    vpc = case.vpc
    vpc.did = "1e9e8a09-18fd-5370-94c3-7297c40e3a46"
    vpc.did_type = "IDFA"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("idfa", vpc.did)
    assertTrackerTags.ad_tag("cid", vpc.did)
    assertTrackerTags.ad_tag("user_id_type", vpc.did_type)
    assertTrackerTags.ad_tag("us_privacy", "1---")


@pytest.mark.regression
def test_tracker_ad_tag_user_info_valid_values_CID():
    case = Case("test_tracker_ad_tag_user_info_valid_values_CID")
    vpc = case.vpc
    vpc.did = "1e9e8a09-18fd-5370-94c3-7297c40e3a46"
    vpc.did_type = "CID"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("idfa", "")
    assertTrackerTags.ad_tag("cid", vpc.did)
    assertTrackerTags.ad_tag("user_id_type", vpc.did_type)
    assertTrackerTags.ad_tag("us_privacy", "1---")


@pytest.mark.regression
def test_tracker_ad_tag_user_info_valid_values_AFAI():
    case = Case("test_tracker_ad_tag_user_info_valid_values_AFAI")
    vpc = case.vpc
    vpc.did = "1e9e8a09-18fd-5370-94c3-7297c40e3a46"
    vpc.did_type = "AFAI"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("idfa", "")
    assertTrackerTags.ad_tag("cid", vpc.did)
    assertTrackerTags.ad_tag("user_id_type", vpc.did_type)
    assertTrackerTags.ad_tag("us_privacy", "1---")


@pytest.mark.regression
def test_tracker_ad_tag_user_info_valid_values_MSAI():
    case = Case("test_tracker_ad_tag_user_info_valid_values_MSAI")
    vpc = case.vpc
    vpc.did = "1e9e8a09-18fd-5370-94c3-7297c40e3a46"
    vpc.did_type = "MSAI"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("idfa", "")
    assertTrackerTags.ad_tag("cid", vpc.did)
    assertTrackerTags.ad_tag("user_id_type", vpc.did_type)
    assertTrackerTags.ad_tag("us_privacy", "1---")


@pytest.mark.regression
def test_tracker_ad_tag_user_info_valid_values_RIDA():
    case = Case("test_tracker_ad_tag_user_info_valid_values_RIDA")
    vpc = case.vpc
    vpc.did = "1e9e8a09-18fd-5370-94c3-7297c40e3a46"
    vpc.did_type = "RIDA"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("idfa", "")
    assertTrackerTags.ad_tag("cid", vpc.did)
    assertTrackerTags.ad_tag("user_id_type", vpc.did_type)
    assertTrackerTags.ad_tag("us_privacy", "1---")


@pytest.mark.regression
def test_tracker_ad_tag_user_info_valid_values_TVOS():
    case = Case("test_tracker_ad_tag_user_info_valid_values_TVOS")
    vpc = case.vpc
    vpc.did = "1e9e8a09-18fd-5370-94c3-7297c40e3a46"
    vpc.did_type = "TVOS"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("idfa", "")
    assertTrackerTags.ad_tag("cid", vpc.did)
    assertTrackerTags.ad_tag("user_id_type", vpc.did_type)
    assertTrackerTags.ad_tag("us_privacy", "1---")
