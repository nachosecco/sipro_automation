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


@description("Test when personal data consent provided as 1, all media tags are blank")
@pytest.mark.regression
def test_tag_media_gpp_personal_data_consent_flag_as_no_consent():
    case = Case("test_tag_media_gpp_personal_data_consent_flag_as_no_consent")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BAAAAAAABAA.QA"
    vpc.geo_co = "US"
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@description(
    "Test when personal data consent provided as 0 (not applicable), all media tags retains value"
)
@pytest.mark.regression
def test_tag_media_gpp_personal_data_consent_flag_as_not_applicable():
    case = Case("test_tag_media_gpp_personal_data_consent_flag_as_not_applicable")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BAAAAAAAAAA.QA"
    vpc.geo_co = "US"
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.ua, vpc.did)


@description(
    "Test when personal data consent provided as 2 (Consent), all media tags retains value"
)
@pytest.mark.regression
def test_tag_media_gpp_personal_data_consent_flag_as_consent():
    case = Case("test_tag_media_gpp_personal_data_consent_flag_as_consent")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BAAAAAAACAA.QA"
    vpc.geo_co = "US"
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.ua, vpc.did)


@description(
    "Test when personal data consent provided as 1, liveramp cookie sync url is removed"
)
@pytest.mark.regression
def test_gpp_personal_data_consent_flag_no_consent_liveramp_cookie_sync_url_removed():
    case = Case(
        "test_gpp_personal_data_consent_flag_no_consent_liveramp_cookie_sync_url_removed"
    )

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vpc.gpp = "DBABLA~BAAAAAAABAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "http://idsync.rlcdn.com"
    )


@description(
    "Test when personal data consent provided as 0, liveramp cookie sync url is retained"
)
@pytest.mark.regression
def test_gpp_personal_data_consent_flag_not_applicable_liveramp_cookie_sync_url_retained():
    case = Case(
        "test_gpp_personal_data_consent_flag_not_applicable_liveramp_cookie_sync_url_retained"
    )

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vpc.gpp = "DBABLA~BAAAAAAAAAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionContainsText("https://idsync.rlcdn.com")


@description(
    "Test when personal data consent provided as 1 (no consent), bidder cookie sync url is removed"
)
@pytest.mark.regression
def test_gpp_personal_data_consent_flag_no_consent_bidder_cookie_sync_url_removed():
    case = Case(
        "test_gpp_personal_data_consent_flag_no_consent_bidder_cookie_sync_url_removed"
    )

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vpc.gpp = "DBABLA~BAAAAAAABAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "https://cookiesyncurl.net"
    )


@description(
    "Test when personal data consent provided as 2 (consent), bidder cookie sync url retained"
)
@pytest.mark.regression
def test_gpp_personal_data_consent_flag_as_consent_bidder_cookie_sync_url_retained():
    case = Case(
        "test_gpp_personal_data_consent_flag_as_consent_bidder_cookie_sync_url_retained"
    )

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BAAAAAAACAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionContainsText("https://cookiesyncurl.net")
