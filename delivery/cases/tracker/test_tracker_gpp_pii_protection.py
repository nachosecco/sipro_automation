import pytest
from core.case import Case
from core.enums.gppSection import GPPSection

from core.Description import description
from core.utils.geoIpUtils import get_ip_for_geo
from core.vastValidator import VastValidator


@description(
    "PII is not hidden from tracker url when sale opt notice is not applicable and opted out"
)
@pytest.mark.regression
def test_gpp_tracker_sale_opt_out_false_when_notice_is_zero_opt_out_is_one():
    case = Case(
        "test_gpp_tracker_sale_opt_out_false_when_notice_is_zero_opt_out_is_one"
    )
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABJg~BAQAAAA.QA"  # notice = 0, saleOptOut = 1
    vpc.gpp_sid = GPPSection.COLORADO.id
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
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

    # This will execute the all assertions in the case
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assert_tracker_tags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assert_tracker_tags.ad_tag("geo_co", vpc.geo_co)
    assert_tracker_tags.ad_tag("geo_dma", vpc.geo_dma)
    assert_tracker_tags.ad_tag("geo_sub", vpc.geo_sub)
    assert_tracker_tags.ad_tag("geo_subname", vpc.geo_subname)
    assert_tracker_tags.ad_tag("geo_code", vpc.geo_code)
    assert_tracker_tags.ad_tag("geo_conn_type", vpc.geo_conn_type)
    assert_tracker_tags.ad_tag("geo_ip", vpc.geo_ip)
    assert_tracker_tags.ad_tag("geo_lat", vpc.geo_lat)
    assert_tracker_tags.ad_tag("geo_long", vpc.geo_long)
    assert_tracker_tags.ad_tag("geo_isp_name", vpc.geo_isp_name)
    assert_tracker_tags.ad_tag("device_id", vpc.did)
    assert_tracker_tags.ad_tag("cid", vpc.did)
    assert_tracker_tags.ad_tag("ua", vpc.ua)


@description(
    "PII is hidden from tracker urls when sale opt notice is not provided and not opted out"
)
@pytest.mark.regression
def test_gpp_tracker_sale_opt_out_true_when_notice_is_two_optOut_is_two():
    case = Case("test_gpp_tracker_sale_opt_out_true_when_notice_is_two_optOut_is_two")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe"
    vpc.geo_co = "US"
    vpc.gpp = "DBABJg~BIgAAAA.QA"  # saleOptOut = 2
    vpc.gpp_sid = GPPSection.COLORADO.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assert_tracker_tags = vastResult.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assert_tracker_tags.ad_tag("geo_co", "")
    assert_tracker_tags.ad_tag("geo_dma", "")
    assert_tracker_tags.ad_tag("geo_sub", "")
    assert_tracker_tags.ad_tag("geo_subname", "")
    assert_tracker_tags.ad_tag("geo_code", "")
    assert_tracker_tags.ad_tag("geo_conn_type", "")
    assert_tracker_tags.ad_tag("geo_ip", "")
    assert_tracker_tags.ad_tag("geo_lat", "")
    assert_tracker_tags.ad_tag("geo_long", "")
    assert_tracker_tags.ad_tag("geo_isp_name", "")
    assert_tracker_tags.ad_tag("device_id", "")
    assert_tracker_tags.ad_tag("cid", "")
    assert_tracker_tags.ad_tag("ua", "")
