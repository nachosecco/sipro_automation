import pytest
from core.case import Case
from core.enums.gppSection import GPPSection
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_geo_for_ip
from core.utils.piiMediaTagUtils import (
    assert_all_media_ad_tags,
    assert_all_media_ad_tags_blank,
)
from core.Description import description


@description(
    "PII is not hidden from media tags when sale opt notice is not applicable and opted out"
)
@pytest.mark.regression
def test_gpp_tag_sale_opt_out_false_when_notice_is_zero_opt_out_is_any():
    case = Case("test_gpp_tag_sale_opt_out_false_when_notice_is_zero_opt_out_is_any")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABJg~BAQAAAA.QA"  # notice = 0, saleOptOut = 1
    vpc.geo_co = "US"
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.gpp_sid = GPPSection.COLORADO.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.ua, vpc.did)


@description(
    "PII is hidden from media tags when sale opt notice is not provided and not opted out"
)
@pytest.mark.regression
def test_gpp_tag_sale_opt_out_true_when_notice_is_two_optOut_is_any():
    case = Case("test_gpp_tag_sale_opt_out_true_when_notice_is_two_optOut_is_any")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe"
    vpc.geo_co = "US"
    vpc.gpp = "DBABJg~BIgAAAA.QA"  # saleOptOut = 2
    vpc.gpp_sid = GPPSection.COLORADO.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@description(
    "Liveramp cookie sync url is removed when sale opt notice is provided and opt out is not applicable"
)
@pytest.mark.regression
def test_gpp_tag_sale_opt_true_liveramp_cookie_sync_url_removed():
    case = Case("test_gpp_tag_sale_opt_true_liveramp_cookie_sync_url_removed")

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vpc.gpp = "DBABJg~BEAAAAA.QA"
    vpc.gpp_sid = GPPSection.COLORADO.id
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "http://idsync.rlcdn.com"
    )


@description(
    "Bidder cookie sync url is removed when sale opt notice is provided and opted out"
)
@pytest.mark.regression
def test_gpp_tag_sale_opt_true_bidder_cookie_sync_url_removed():
    case = Case("test_gpp_tag_sale_opt_true_bidder_cookie_sync_url_removed")

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vpc.gpp = "DBABJg~BEQAAAA.QA"
    vpc.gpp_sid = GPPSection.COLORADO.id
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "https://cookiesyncurl.net"
    )
