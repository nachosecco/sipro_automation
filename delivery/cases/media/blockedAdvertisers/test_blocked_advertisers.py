import pytest

from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_delivery_automation_blocked_advertisers():
    """
    This case uses a placement with a media aligned that has ford.com as advertiser url
    Expected is that after sending the value as blocked advertiser, media won't return
    """
    case = Case("test_delivery_automation_blocked_advertisers")
    vpc = case.vpc
    vpc.badv = "ford.com"
    vast = VastValidator().test(vpc)
    vast.assertCase(case)
    vast.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
def test_should_block_media_because_not_informed_blocked_advertiser():
    """
    This case uses a placement with a media aligned that do not have an advertiser url
    Expected is that after sending any value as blocked advertiser, media won't return
    Conservative approach
    """
    case = Case("test_should_block_media_because_not_informed_blocked_advertiser")
    vpc = case.vpc
    vpc.badv = "any-value.com"
    vast = VastValidator().test(vpc)
    vast.assertCase(case)
    vast.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
def test_should_not_block_media_because_not_sent_blocked_advertiser():
    """
    This case uses a placement with a media aligned that has ford.com as advertiser url
    Expected is that the media is returned given that we are not sending badv
    """
    case = Case("test_should_not_block_media_because_not_sent_blocked_advertiser")
    vpc = case.vpc
    vast = VastValidator().test(vpc)
    vast.assertCase(case)
    vast.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_should_not_block_media_because_not_matching_blocked_advertiser():
    """
    This case uses a placement with a media aligned that has ford.com as advertiser url
    Expected is that the media is returned given that the value sent is not matching media advertiser
    """
    case = Case("test_should_not_block_media_because_not_matching_blocked_advertiser")
    vpc = case.vpc
    vpc.badv = "www.chevrolet.com"
    vast = VastValidator().test(vpc)
    vast.assertCase(case)
    vast.assert_vast_xml().assert_ad_count(1)
