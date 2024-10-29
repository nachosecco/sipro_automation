import pytest
from core.case import Case

from core.vastValidator import VastValidator


# validating the Geo tracker information for the impression node from the vast response with valid values
@pytest.mark.regression
def test_tracker_ad_tag_geo_info_valid_values():
    case = Case("test_tracker_ad_tag_geo_info_valid_values")
    vpc = case.vpc
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

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("geo_co", vpc.geo_co)
    assertTrackerTags.ad_tag("geo_dma", vpc.geo_dma)
    assertTrackerTags.ad_tag("geo_sub", vpc.geo_sub)
    assertTrackerTags.ad_tag("geo_subname", vpc.geo_subname)
    assertTrackerTags.ad_tag("geo_code", vpc.geo_code)
    assertTrackerTags.ad_tag("geo_conn_type", vpc.geo_conn_type)
    assertTrackerTags.ad_tag("geo_ip", vpc.geo_ip)
    assertTrackerTags.ad_tag("geo_lat", vpc.geo_lat)
    assertTrackerTags.ad_tag("geo_long", vpc.geo_long)
    assertTrackerTags.ad_tag("geo_isp_name", vpc.geo_isp_name)


# validating the Geo tracker information for the impression node from the vast response with empty values
@pytest.mark.regression
def test_tracker_ad_tag_geo_info_empty_values():
    case = Case("test_tracker_ad_tag_geo_info_empty_values")
    vpc = case.vpc
    vpc.geo_co = "geo_co"
    vpc.geo_ip = "52.13.119.116"
    vpc.geo_dma = ""
    vpc.geo_lat = ""
    vpc.geo_sub = ""
    vpc.geo_code = ""
    vpc.geo_long = ""
    vpc.geo_conn_type = ""
    vpc.geo_isp_name = ""
    vpc.geo_subname = ""
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertTrackerTags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assertTrackerTags.ad_tag("geo_co", vpc.geo_co)
    assertTrackerTags.ad_tag("geo_dma", vpc.geo_dma)
    assertTrackerTags.ad_tag("geo_sub", vpc.geo_sub)
    assertTrackerTags.ad_tag("geo_subname", vpc.geo_subname)
    assertTrackerTags.ad_tag("geo_code", vpc.geo_code)
    assertTrackerTags.ad_tag("geo_conn_type", vpc.geo_conn_type)
    assertTrackerTags.ad_tag("geo_ip", vpc.geo_ip)
    assertTrackerTags.ad_tag("geo_lat", vpc.geo_lat)
    assertTrackerTags.ad_tag("geo_long", vpc.geo_long)
    assertTrackerTags.ad_tag("geo_isp_name", vpc.geo_isp_name)
