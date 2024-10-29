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


@description(
    "PII is not hidden from media tags when known child sensitive data consents is 2_0"
)
@pytest.mark.regression
def test_gpp_tag_known_child_sensitive_data_consents_false_when_2_0():
    case = Case("test_gpp_tag_known_child_sensitive_data_consents_false_when_2_0")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BAAAAAAAgAA.QA"  # consents = 2,0
    vpc.geo_co = "US"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.ua, vpc.did)


@description(
    "PII is hidden from media tags when known child sensitive data consents is 1_0"
)
@pytest.mark.regression
def test_gpp_tag_known_child_sensitive_data_consents_true_when_1_0():
    case = Case("test_gpp_tag_known_child_sensitive_data_consents_true_when_1_0")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe"
    vpc.geo_co = "US"
    vpc.gpp = "DBABLA~BAAAAAAAQAA.QA"  # consents = 1,0
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@description(
    "PII is hidden from media tags when known child sensitive data consents is 1 for virginia"
)
@pytest.mark.regression
def test_gpp_tag_known_child_sensitive_data_consents_true_when_1_for_virginia():
    case = Case(
        "test_gpp_tag_known_child_sensitive_data_consents_true_when_1_for_virginia"
    )
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe"
    vpc.geo_co = "US"
    vpc.gpp = "DBABRg~BAAAAEA"  # consents = 1
    vpc.gpp_sid = GPPSection.VIRGINIA.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@description(
    "PII is not hidden from media tags when known child sensitive data consents is 2 for virginia"
)
@pytest.mark.regression
def test_gpp_tag_known_child_sensitive_data_consents_false_when_2_for_virginia():
    case = Case(
        "test_gpp_tag_known_child_sensitive_data_consents_false_when_2_for_virginia"
    )
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABRg~BAAAAIA"  # consents = 2
    vpc.geo_co = "US"
    vpc.gpp_sid = GPPSection.VIRGINIA.id
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.ua, vpc.did)


@description(
    "Liveramp cookie sync url is removed from media tags when known child sensitive data_consents_true_no_consent"
)
@pytest.mark.regression
def test_gpp_tag_known_child_sensitive_data_consents_true_liveramp_url_removed():
    case = Case(
        "test_gpp_tag_known_child_sensitive_data_consents_true_liveramp_url_removed"
    )

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vpc.gpp = "DBABLA~BAAAAAAAQAA.QA"  # consents = 1,0
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "http://idsync.rlcdn.com"
    )


@description(
    "Bidder cookie sync url is removed from media tags when known child sensitive data_consents_true_no_consent"
)
@pytest.mark.regression
def test_gpp_tag_known_child_sensitive_data_consents_true_bidder_url_removed():
    case = Case(
        "test_gpp_tag_known_child_sensitive_data_consents_true_bidder_url_removed"
    )

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vpc.gpp = "DBABLA~BAAAAAAAEAA.QA"  # consents = 0,1
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "https://cookiesyncurl.net"
    )
