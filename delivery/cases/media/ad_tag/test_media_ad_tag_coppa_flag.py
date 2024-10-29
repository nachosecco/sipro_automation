import pytest

from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_geo_for_ip


@pytest.mark.regression
def test_media_ad_tag_coppa_flag_set_to_true():
    case = Case("test_media_ad_tag_coppa_flag_set_to_true")
    vpc = case.vpc
    # geo properties
    vpc.coppa = "1"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.app_id = "c6app"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="New York", city="Brooklyn", postcode="11206"
    )

    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("geo_ip", "")
    assertMediaTags.ad_tag("geo_lat", "")
    assertMediaTags.ad_tag("geo_long", "")
    assertMediaTags.ad_tag("geo_latlng", "")
    assertMediaTags.ad_tag("idfa", "")
    assertMediaTags.ad_tag("adv_id", "")
    assertMediaTags.ad_tag("app_id", vpc.app_id)
    assertMediaTags.ad_tag("device_id", "")
    assertMediaTags.ad_tag("cid", "")
    assertMediaTags.ad_tag("idfa", "")


@pytest.mark.regression
def test_media_ad_tag_coppa_flag_set_to_false():
    case = Case("test_media_ad_tag_coppa_flag_set_to_false")
    vpc = case.vpc
    # geo properties
    vpc.coppa = "0"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.app_id = "c6app"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="New York", city="Brooklyn", postcode="11206"
    )

    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo_data = get_geo_for_ip(vpc.ip_address)
    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("geo_ip", vpc.ip_address)
    assertMediaTags.ad_tag("geo_lat", geo_data["lat"])
    assertMediaTags.ad_tag("geo_long", geo_data["lon"])
    assertMediaTags.ad_tag("geo_latlng", f"{geo_data['lat']},{geo_data['lon']}")
    assertMediaTags.ad_tag("app_id", vpc.app_id)
    assertMediaTags.ad_tag("device_id", vpc.did)
    assertMediaTags.ad_tag("cid", vpc.did)
    assertMediaTags.ad_tag("idfa", vpc.did)


@pytest.mark.regression
def test_media_ad_tag_coppa_flag_set_to_OtherValue():
    case = Case("test_media_ad_tag_coppa_flag_set_to_OtherValue")
    vpc = case.vpc
    vpc.coppa = "2"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.app_id = "c6app"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="New York", city="Brooklyn", postcode="11206"
    )

    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo_data = get_geo_for_ip(vpc.ip_address)
    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("geo_ip", vpc.ip_address)
    assertMediaTags.ad_tag("geo_lat", geo_data["lat"])
    assertMediaTags.ad_tag("geo_long", geo_data["lon"])
    assertMediaTags.ad_tag("geo_latlng", f"{geo_data['lat']},{geo_data['lon']}")
    assertMediaTags.ad_tag("app_id", vpc.app_id)
    assertMediaTags.ad_tag("device_id", vpc.did)
    assertMediaTags.ad_tag("cid", vpc.did)
    assertMediaTags.ad_tag("idfa", vpc.did)
