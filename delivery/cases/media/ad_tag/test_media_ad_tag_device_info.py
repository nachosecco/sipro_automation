import pytest
from core.case import Case
from core.constants import ComparisonType
from core.devices import DEVICE_CTV_ROKU
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_ad_tag_device_info_valid_values():
    case = Case("test_media_ad_tag_device_info_valid_values")
    vpc = case.vpc
    vpc.ua = DEVICE_CTV_ROKU.ua
    vpc.did = "3824add4-6141-5a8b-9b85-d88c2ff781b1"
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("ua", vpc.ua)
    assertMediaTags.ad_tag("osplatform", DEVICE_CTV_ROKU.os.lower())
    assertMediaTags.ad_tag("osv", DEVICE_CTV_ROKU.os_version)
    assertMediaTags.ad_tag("osvmajor", "")
    assertMediaTags.ad_tag("osvminor", "")
    assertMediaTags.ad_tag("devicecategory", DEVICE_CTV_ROKU.targeting_type.lower())
    assertMediaTags.ad_tag("devicemake", DEVICE_CTV_ROKU.make)
    assertMediaTags.ad_tag("devicemodel", DEVICE_CTV_ROKU.model)
    assertMediaTags.ad_tag("device_id", vpc.did)


@pytest.mark.regression
def test_media_ad_tag_device_info_empty_values():
    case = Case("test_media_ad_tag_device_info_empty_values")
    vpc = case.vpc
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("ua", "python-requests/", ComparisonType.Startswith)
    assertMediaTags.ad_tag("osplatform", "other")
    assertMediaTags.ad_tag("osv", "")
    assertMediaTags.ad_tag("osvmajor", "")
    assertMediaTags.ad_tag("osvminor", "")
    assertMediaTags.ad_tag("devicecategory", "unknown")
    assertMediaTags.ad_tag("devicemake", "")
    assertMediaTags.ad_tag("devicemodel", "")
