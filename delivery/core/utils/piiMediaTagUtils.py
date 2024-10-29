from core.utils.geoIpUtils import get_geo_for_ip


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
    assert_media_tags.ad_tag("geo_latlng", "")
    assert_media_tags.ad_tag("geo_isp_name", "")
    assert_media_tags.ad_tag("device_id", "")
    assert_media_tags.ad_tag("cid", "")
    assert_media_tags.ad_tag("idfa", "")
    assert_media_tags.ad_tag("adv_id", "")
    assert_media_tags.ad_tag("ua", "")


def assert_all_media_ad_tags(vast_result, ip_address, ua, did, device_type="cid"):
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
    assert_media_tags.ad_tag(device_type, did)
    assert_media_tags.ad_tag("ua", ua)


def assert_precise_location_media_tags_blank(vast_result, expected_country):
    assert_media_tags = vast_result.assertXML().assertMediaTags()
    assert_media_tags.ad_tag("geo_code", "")
    assert_media_tags.ad_tag("geo_ip", "")
    assert_media_tags.ad_tag("geo_lat", "")
    assert_media_tags.ad_tag("geo_long", "")
    assert_media_tags.ad_tag("geo_co", expected_country)
