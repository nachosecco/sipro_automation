import pytest
from core.case import Case
from core.enums.gppSection import GPPSection
from core.utils.piiMediaTagUtils import (
    assert_all_media_ad_tags,
    assert_all_media_ad_tags_blank,
)

from core.Description import description
from core.utils.geoIpUtils import get_ip_for_geo
from core.vastValidator import VastValidator


@description("Test when share notice provided as 1, media tags retains value")
@pytest.mark.regression
def test_gpp_share_notice_enabled_virginia():
    case = Case("test_gpp_share_notice_enabled_virginia")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABRg~BQAAABA"
    vpc.geo_co = "US"
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.gpp_sid = GPPSection.VIRGINIA.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.ua, vpc.did)


@description("Test when share notice provided as 2, all media tag are blank")
@pytest.mark.regression
def test_gpp_share_notice_disabled_virginia():
    case = Case("test_gpp_share_notice_disabled_virginia")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe"
    vpc.geo_co = "US"
    vpc.gpp = "DBABRg~BgAAABA"
    vpc.gpp_sid = GPPSection.VIRGINIA.id
    vpc.did_type = "idfa"
    vpc.add_custom_param("adv_id", "randomId")
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@description("Test when share notice provided as 0, media tags retains value")
@pytest.mark.regression
def test_gpp_share_notice_enabled_colorado():
    case = Case("test_gpp_share_notice_enabled_colorado")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5d"
    vpc.gpp = "DBABJg~BAAAAEA.QA"
    vpc.geo_co = "US"
    vpc.gpp_sid = GPPSection.COLORADO.id
    vpc.did_type = "idfa"
    vpc.add_custom_param("adv_id", "232a34233fea")
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.ua, vpc.did, vpc.did_type)


@description(
    "Test when share notice provided as 2, liveramp cookie sync url is removed"
)
@pytest.mark.regression
def test_gpp_share_notice_disabled_liveramp_cookie_sync_url_removed():
    case = Case("test_gpp_share_notice_disabled_liveramp_cookie_sync_url_removed")

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vpc.gpp = "DBABVg~BgAAAAEA.QA"
    vpc.gpp_sid = GPPSection.CONNECTICUT.id
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "http://idsync.rlcdn.com"
    )


@description("Test when share notice provided as 1, liveramp cookie sync url exists")
@pytest.mark.regression
def test_gpp_share_notice_enabled_liveramp_cookie_sync_url_present():
    case = Case("test_gpp_share_notice_enabled_liveramp_cookie_sync_url_present")

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABVg~BQAAAAEA.QA"
    vpc.gpp_sid = GPPSection.CONNECTICUT.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionContainsText("https://idsync.rlcdn.com")


@description("Test when share notice provided as 2, bidder cookie sync url is removed")
@pytest.mark.regression
def test_gpp_share_notice_disabled_bidder_cookie_sync_url_removed():
    case = Case("test_gpp_share_notice_disabled_bidder_cookie_sync_url_removed")

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vpc.gpp = "DBABVg~BgAAAAEA.QA"
    vpc.gpp_sid = GPPSection.CONNECTICUT.id
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "https://cookiesyncurl.net"
    )


@description("Test when share notice provided as 1, bidder cookie sync url exists")
@pytest.mark.regression
def test_gpp_share_notice_enabled_bidder_cookie_sync_url_present():
    case = Case("test_gpp_share_notice_enabled_bidder_cookie_sync_url_present")

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABVg~BQAAAAEA.QA"
    vpc.gpp_sid = GPPSection.CONNECTICUT.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionContainsText("https://cookiesyncurl.net")
