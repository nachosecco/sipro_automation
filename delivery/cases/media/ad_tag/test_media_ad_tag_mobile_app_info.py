import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_ad_tag_mobile_app_valid_values():
    case = Case("test_media_ad_tag_mobile_app_valid_values")
    vpc = case.vpc
    vpc.app_name = "ROKU"
    vpc.app_id = "com.apple.mobilesafari"
    vpc.app_uri = "https://itunes.apple.com"
    vpc.app_ver = "1.2.1"
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery(
        ["ROKU", "com.apple.mobilesafari", "https://itunes.apple.com", "1.2.1"]
    )

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("app_name", vpc.app_name)
    assertMediaTags.ad_tag("app_id", vpc.app_id)
    assertMediaTags.ad_tag("app_uri", vpc.app_uri)
    assertMediaTags.ad_tag("app_ver", vpc.app_ver)


@pytest.mark.regression
def test_media_ad_tag_mobile_app_empty_values():
    case = Case("test_media_ad_tag_mobile_app_empty_values")
    vpc = case.vpc
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("app_name", vpc.app_name)
    assertMediaTags.ad_tag("app_id", vpc.app_id)
    assertMediaTags.ad_tag("app_uri", "")
    assertMediaTags.ad_tag("app_ver", vpc.app_ver)
