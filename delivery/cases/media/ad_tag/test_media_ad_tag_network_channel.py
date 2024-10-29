import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.constants import REPLACE

# This test validates the media ad tag network and channel gets values passed via vast request
#  Configuration:
#  Media - Managed media -> Ad tag -> having network and channel tags
@pytest.mark.regression
def test_media_adtag_network_channel():
    case = Case("test_media_adtag_network_channel")
    vpc = case.vpc
    vpc.channel_name = "test_channel"
    vpc.network_name = "test_network"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("network", vpc.network_name)
    assertMediaTags.ad_tag("channel", vpc.channel_name)


# This test validates the media ad tag network and channel gets values passed via vast request
#  Configuration:
#  Media - Managed media -> Ad tag -> having network and channel tags
@pytest.mark.regression
def test_media_adtag_network_channel_empty_values():
    case = Case("test_media_adtag_network_channel_empty_values")
    vpc = case.vpc

    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("network", REPLACE)
    assertMediaTags.ad_tag("channel", REPLACE)
