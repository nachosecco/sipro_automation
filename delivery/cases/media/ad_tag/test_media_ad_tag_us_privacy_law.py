import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_geo_for_ip
from core.did import DID_WITH_NO_AUDIENCE_TARGETING, DID_WITH_AUDIENCE_TARGETING


def assert_all_media_ad_tags_blank(vast_result):
    assert_media_tags = vast_result.assertXML().assertMediaTags()
    assert_media_tags.ad_tag("geo_co", "")
    assert_media_tags.ad_tag("geo_dma", "")
    assert_media_tags.ad_tag("geo_sub", "")
    assert_media_tags.ad_tag("geo_subname", "")
    assert_media_tags.ad_tag("geo_code", "")
    assert_media_tags.ad_tag("geo_conn_type", "")
    assert_media_tags.ad_tag("geo_ip", "")
    assert_media_tags.ad_tag("geo_lat", "")
    assert_media_tags.ad_tag("geo_long", "")
    assert_media_tags.ad_tag("geo_isp_name", "")
    assert_media_tags.ad_tag("device_id", "")
    assert_media_tags.ad_tag("cid", "")


def assert_all_media_ad_tags(vast_result, ip_address, did):
    geo_data = get_geo_for_ip(ip_address)
    assert_media_tags = vast_result.assertXML().assertMediaTags()
    assert_media_tags.ad_tag("geo_co", geo_data["country"])
    assert_media_tags.ad_tag("geo_dma", geo_data["dma"])
    assert_media_tags.ad_tag("geo_sub", geo_data["region_iso_code"])
    assert_media_tags.ad_tag("geo_subname", geo_data["region"])
    assert_media_tags.ad_tag("geo_code", geo_data["postcode"])
    assert_media_tags.ad_tag("geo_conn_type", geo_data["connection_type"])
    assert_media_tags.ad_tag("geo_ip", ip_address)
    assert_media_tags.ad_tag("geo_lat", geo_data["lat"])
    assert_media_tags.ad_tag("geo_long", geo_data["lon"])
    assert_media_tags.ad_tag("geo_isp_name", geo_data["carrier"])
    assert_media_tags.ad_tag("device_id", did)
    assert_media_tags.ad_tag("cid", did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_enabled_california():
    case = Case("test_media_ad_tag_us_privacy_law_enabled_california")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1YYY"
    vpc.ip_address = get_ip_for_geo(country="US", region="California")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_enabled_california_1NYY():
    case = Case("test_media_ad_tag_us_privacy_law_enabled_california_1NYY")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1YYY"
    vpc.ip_address = get_ip_for_geo(country="US", region="California")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_california():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_california")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING

    vpc.us_privacy = "1NNN"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="California", postcode="93501", dma="803"
    )
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_blank_california():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_blank_california")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1---"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="California", postcode="93501", dma="803"
    )
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_enabled_NewYork():
    case = Case("test_media_ad_tag_us_privacy_law_enabled_NewYork")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1YYY"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="New York", city="Brooklyn", postcode="11206", dma="501"
    )
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_NewYork():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_NewYork")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1NNN"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="New York", city="Brooklyn", postcode="11206", dma="501"
    )
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_blank_NewYork():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_blank_NewYork")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1---"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="New York", city="Brooklyn", postcode="11206", dma="501"
    )
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_enabled_Virginia():
    case = Case("test_media_ad_tag_us_privacy_law_enabled_Virginia")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1YYY"
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_Virginia():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_Virginia")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1NNN"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Virginia", postcode="22901", dma="584"
    )
    vast_result = VastValidator().test(vpc)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_blank_Virginia():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_blank_Virginia")

    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1---"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Virginia", postcode="22901", dma="584"
    )
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_us_privacy_law_enabled_bidder_cookie_sync_url_removed():
    case = Case("test_us_privacy_law_enabled_bidder_cookie_sync_url_removed")

    vpc = case.vpc
    vpc.us_privacy = "1YYY"
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.ip_address = get_ip_for_geo(country="US", region="California")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "https://cookiesyncurl.net"
    )


@pytest.mark.regression
def test_us_privacy_law_enabled_liveramp_cookie_sync_url_removed():
    case = Case("test_us_privacy_law_enabled_liveramp_cookie_sync_url_removed")

    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.ip_address = get_ip_for_geo(country="US", region="California")
    vpc.us_privacy = "1YYY"
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionNotContainsText(
        "http://idsync.rlcdn.com"
    )


@pytest.mark.regression
def test_us_privacy_law_disabled_bidder_cookie_sync_url_present():
    case = Case("test_us_privacy_law_disabled_bidder_cookie_sync_url_present")

    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.ip_address = get_ip_for_geo(country="US", region="California")
    vpc.us_privacy = "1NNN"
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionContainsText("https://cookiesyncurl.net")


@pytest.mark.regression
def test_us_privacy_law_disabled_liveramp_cookie_sync_url_present():
    case = Case("test_us_privacy_law_disabled_liveramp_cookie_sync_url_present")

    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.ip_address = get_ip_for_geo(country="US", region="California")
    vpc.us_privacy = "1NNN"
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertXML().assertTagImpressionContainsText("https://idsync.rlcdn.com")


@pytest.mark.regression
def test_media_us_privacy_law_enabled_audience_targeting_applied():
    case = Case("test_media_us_privacy_law_enabled_audience_targeting_applied")

    vpc = case.vpc
    vpc.us_privacy = "1YYY"
    vpc.did = DID_WITH_AUDIENCE_TARGETING
    vpc.ip_address = get_ip_for_geo(country="US", region="California")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    vast_result.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_media_us_privacy_law_disabled_audience_targeting_applied():
    case = Case("test_media_us_privacy_law_disabled_audience_targeting_applied")

    vpc = case.vpc
    vpc.us_privacy = "1NNN"
    vpc.did = DID_WITH_AUDIENCE_TARGETING
    vpc.ip_address = get_ip_for_geo(country="US", region="California")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    vast_result.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_enabled_colorado():
    case = Case("test_media_ad_tag_us_privacy_law_enabled_colorado")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1YYY"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_colorado():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_colorado")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1NNN"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Colorado", postcode="80204", dma="751"
    )
    vast_result = VastValidator().test(vpc)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_blank_colorado():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_blank_colorado")

    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1---"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Colorado", postcode="80204", dma="751"
    )
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_enabled_connecticut():
    case = Case("test_media_ad_tag_us_privacy_law_enabled_connecticut")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1YYY"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_connecticut():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_connecticut")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1NNN"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Connecticut", postcode="06470", dma="501"
    )
    vast_result = VastValidator().test(vpc)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_disabled_blank_connecticut():
    case = Case("test_media_ad_tag_us_privacy_law_disabled_blank_connecticut")

    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1---"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Connecticut", postcode="06470", dma="501"
    )
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.did)


@description("Test the private law enabled in utah")
@pytest.mark.regression
def test_media_ad_tag_us_privacy_law_enabled_utah():
    case = Case("test_media_ad_tag_us_privacy_law_enabled_utah")
    vpc = case.vpc
    vpc.did = DID_WITH_NO_AUDIENCE_TARGETING
    vpc.us_privacy = "1YYY"
    vpc.ip_address = get_ip_for_geo(country="US", region="Utah")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags_blank(vast_result)
