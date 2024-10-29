import pytest
from core.case import Case
from core.constants import ComparisonType
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_delivery_automation_media_ad_tag_lmt_pass_values_1():
    case = Case("test_delivery_automation_media_ad_tag_lmt_pass_values_1")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.lmt = "1"
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("lmt", vpc.lmt)
    assertMediaTags.ad_tag("device_id", "")
    vastResult.assertLogsDelivery(["lmt=1"])


@pytest.mark.regression
def test_delivery_automation_media_ad_tag_lmt_pass_values_0():
    case = Case("test_delivery_automation_media_ad_tag_lmt_pass_values_0")
    vpc = case.vpc
    vpc.lmt = "0"
    vpc.did = "3824add4-6141-5a8b-9b85-d88c2ff781b1"
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("lmt", vpc.lmt)
    assertMediaTags.ad_tag("device_id", vpc.did)
    vastResult.assertLogsDelivery(["lmt=0"])


@pytest.mark.regression
def test_delivery_automation_media_ad_tag_lmt_pass_invalid_values_11():
    case = Case("test_delivery_automation_media_ad_tag_lmt_pass_invalid_values_11")
    vpc = case.vpc
    vpc.lmt = "11"
    vpc.did = "3824add4-6141-5a8b-9b85-d88c2ff781b1"
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("lmt", "0")
    assertMediaTags.ad_tag("device_id", vpc.did)
    vastResult.assertLogsDelivery(["lmt=11"])
