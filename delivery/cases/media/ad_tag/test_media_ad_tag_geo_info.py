import pytest
from core.case import Case
from core.constants import REPLACE, ComparisonType, IP_ADDRESS_VALIDATION_REGEX

from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_ad_tag_geo_info_valid_values():
    case = Case("test_media_ad_tag_geo_info_valid_values")
    vpc = case.vpc
    # geo properties
    vpc.geo_co = "US"
    vpc.geo_dma = "New York"
    vpc.geo_sub = "sub"
    vpc.geo_subname = "subname"
    vpc.geo_code = "NY"
    vpc.geo_conn_type = "conn_type"
    vpc.geo_ip = "127.0.0.1"
    vpc.geo_lat = "23423.22"
    vpc.geo_long = "23423.23"
    vpc.geo_isp_name = "isp_name"
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("geo_co", vpc.geo_co)
    assertMediaTags.ad_tag("geo_dma", vpc.geo_dma)
    assertMediaTags.ad_tag("geo_sub", vpc.geo_sub)
    assertMediaTags.ad_tag("geo_subname", vpc.geo_subname)
    assertMediaTags.ad_tag("geo_code", vpc.geo_code)
    assertMediaTags.ad_tag("geo_conn_type", vpc.geo_conn_type)
    assertMediaTags.ad_tag("geo_ip", vpc.geo_ip)
    assertMediaTags.ad_tag("geo_lat", vpc.geo_lat)
    assertMediaTags.ad_tag("geo_long", vpc.geo_long)
    assertMediaTags.ad_tag("geo_isp_name", vpc.geo_isp_name)


@pytest.mark.regression
def test_media_ad_tag_geo_info_empty_values():
    case = Case("test_media_ad_tag_geo_info_empty_values")
    vpc = case.vpc
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("geo_co", REPLACE)
    assertMediaTags.ad_tag("geo_dma", REPLACE)
    assertMediaTags.ad_tag("geo_sub", REPLACE)
    assertMediaTags.ad_tag("geo_subname", REPLACE)
    assertMediaTags.ad_tag("geo_code", REPLACE)
    assertMediaTags.ad_tag("geo_conn_type", REPLACE)
    assertMediaTags.ad_tag(
        "geo_ip", IP_ADDRESS_VALIDATION_REGEX, ComparisonType.Pattern
    )
    assertMediaTags.ad_tag("geo_lat", "")
    assertMediaTags.ad_tag("geo_long", "")
    assertMediaTags.ad_tag("geo_isp_name", REPLACE)
