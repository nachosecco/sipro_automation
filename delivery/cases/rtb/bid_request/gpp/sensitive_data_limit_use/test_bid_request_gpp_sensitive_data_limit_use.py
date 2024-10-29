import core.utils.piiBidRequestUtils as brUtils
import pytest
from core.case import Case
from core.enums.gppSection import GPPSection

from core.Description import description
from core.utils.geoIpUtils import get_ip_for_geo
from core.vastValidator import VastValidator


@description(
    "Precise location fields are hidden from bid request ver 2.6 when sensitive data geo notice is provided and opted "
    "out"
)
@pytest.mark.regression
def test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_1_rtb26():
    case = Case(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_1_rtb26"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BABAAAEAAAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_1_rtb26"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    device_geo = bid_request_validator.get_device_geo_object()
    brUtils.is_precise_location_fields_removed(device_geo)
    user_geo = bid_request_validator.get_user_geo_object()
    brUtils.is_precise_location_fields_removed(user_geo)
    bid_request_validator.is_device_ip_not_available()


@description(
    "Precise location fields are hidden from bid request ver 2.5 when sensitive data geo notice is provided and opt "
    "out is not applicable"
)
@pytest.mark.regression
def test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb25():
    case = Case(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb25"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABLA~BABAAAAAAAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb25"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    device_geo = bid_request_validator.get_device_geo_object()
    brUtils.is_precise_location_fields_removed(device_geo)
    user_geo = bid_request_validator.get_user_geo_object()
    brUtils.is_precise_location_fields_removed(user_geo)
    bid_request_validator.is_device_ip_not_available()


@description(
    "Precise location fields are hidden from bid request ver 2.2 when sensitive data geo notice is provided and opt "
    "out is not applicable"
)
@pytest.mark.regression
def test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb22():
    case = Case(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb22"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABLA~BABAAAAAAAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb22"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    device_geo = bid_request_validator.get_device_geo_object()
    brUtils.is_precise_location_fields_removed(device_geo)
    user_geo = bid_request_validator.get_user_geo_object()
    brUtils.is_precise_location_fields_removed(user_geo)
    bid_request_validator.is_device_ip_not_available()


@description(
    "Precise location fields are hidden from bid request ver 2.3 when sensitive data geo notice is provided and opt "
    "out is not applicable"
)
@pytest.mark.regression
def test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb23():
    case = Case(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb23"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABLA~BABAAAAAAAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_1_optout_0_rtb23"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    device_geo = bid_request_validator.get_device_geo_object()
    brUtils.is_precise_location_fields_removed(device_geo)
    user_geo = bid_request_validator.get_user_geo_object()
    brUtils.is_precise_location_fields_removed(user_geo)
    bid_request_validator.is_device_ip_not_available()


@description(
    "Precise location fields are hidden from bid request ver 2.4 when sensitive data geo notice when sensitive data "
    "processing geo notice is not provided"
)
@pytest.mark.regression
def test_bid_request_gpp_sensitive_data_limit_use_true_notice_2_optout_0_rtb24():
    case = Case(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_2_optout_0_rtb24"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.gpp = "DBABLA~BACAAAAAAAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_gpp_sensitive_data_limit_use_true_notice_2_optout_0_rtb24"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    device_geo = bid_request_validator.get_device_geo_object()
    brUtils.is_precise_location_fields_removed(device_geo)
    user_geo = bid_request_validator.get_user_geo_object()
    brUtils.is_precise_location_fields_removed(user_geo)
    bid_request_validator.is_device_ip_not_available()
