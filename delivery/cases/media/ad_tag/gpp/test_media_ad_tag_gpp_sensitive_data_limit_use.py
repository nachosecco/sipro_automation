import pytest
from core.case import Case
from core.enums.gppSection import GPPSection
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_geo_for_ip
from core.utils.piiMediaTagUtils import (
    assert_all_media_ad_tags,
    assert_precise_location_media_tags_blank,
)
from core.Description import description


@description(
    "Precise location fields are not hidden from media tags when sensitive data processing geo notice is provided and "
    "not opted out"
)
@pytest.mark.regression
def test_gpp_tag_sensitive_data_limit_use_false_when_notice_is_one_opt_out_is_two():
    case = Case(
        "test_gpp_tag_sensitive_data_limit_use_false_when_notice_is_one_opt_out_is_two"
    )
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BABAAAIAAAA.QA"  # Notice=1 , OptOut = 2
    vpc.geo_co = "US"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_all_media_ad_tags(vast_result, vpc.ip_address, vpc.ua, vpc.did)


@description(
    "Precise location fields are hidden from media tags when sensitive data processing geo notice is not provided"
)
@pytest.mark.regression
def test_gpp_tag_sensitive_data_limit_use_true_when_notice_is_two_optOut_is_any():
    case = Case(
        "test_gpp_tag_sensitive_data_limit_use_true_when_notice_is_two_optOut_is_any"
    )
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe"
    vpc.geo_co = "US"
    vpc.gpp = "DBABLA~BACAAAAAAAA.QA"  # Notice=2 , OptOut = 0
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_precise_location_media_tags_blank(vast_result, vpc.geo_co)
