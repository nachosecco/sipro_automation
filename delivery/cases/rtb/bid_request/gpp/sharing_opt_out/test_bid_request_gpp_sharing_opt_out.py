import core.utils.piiBidRequestUtils as brUtils
import pytest
from core.case import Case
from core.configuration import Configuration
from core.enums.gppSection import GPPSection

from core.Description import description
from core.utils.geoIpUtils import get_ip_for_geo
from core.vastValidator import VastValidator


@description(
    "PII is hidden from bid requests v2.6 when sharing opt notice is notice not provided and opted out"
)
@pytest.mark.regression
def test_bid_request_ctv_gpp_sharing_opt_out_true_notice_2_optout_1_rtb26():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_gpp_sharing_opt_out_true_notice_2_optout_1_rtb26"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BCAEAAAAAAA.QA"  # Notice = 2 OptOut = 1

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
        "test_bid_request_ctv_gpp_sharing_opt_out_true_notice_2_optout_1_rtb26"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    assert bid_request_validator.is_device_object_as_expected(
        brUtils.get_expected_device_object_rtb26(), True
    )
    assert bid_request_validator.is_user_as_expected(brUtils.get_expected_user_object())
    assert bid_request_validator.is_source_object_as_expected(
        brUtils.get_expected_source_object_rtb26(root_domain)
    )


@description(
    "PII is hidden from bid requests v2.5 when sharing opt notice is notice provided and opt out is not applicable"
)
@pytest.mark.regression
def test_bid_request_ctv_gpp_sharing_opt_out_true_notice_1_optout_0_rtb25():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_gpp_sharing_opt_out_true_notice_1_optout_0_rtb25"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABLA~BBAAAAAAAAA.QA"  # Notice = 1 OptOut = 0
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
        "test_bid_request_ctv_gpp_sharing_opt_out_true_notice_1_optout_0_rtb25"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    assert bid_request_validator.is_device_object_as_expected(
        brUtils.get_expected_device_object_rtb25(), True
    )
    assert bid_request_validator.is_user_as_expected(brUtils.get_expected_user_object())
    assert bid_request_validator.is_source_object_as_expected(
        brUtils.get_expected_source_object_rtb25(root_domain)
    )


@description(
    "PII is hidden from bid requests v2.3 when sharing opt notice is provided and optedout"
)
@pytest.mark.regression
def test_bid_request_ctv_gpp_sharing_opt_out_true_notice_1_optout_1_rtb23():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_gpp_sharing_opt_out_true_notice_1_optout_1_rtb23"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABLA~BBAEAAAAAAA.QA"  # Notice = 1 OptOut = 1
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
        "test_bid_request_ctv_gpp_sharing_opt_out_true_notice_1_optout_1_rtb23"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    assert bid_request_validator.is_device_object_as_expected(
        brUtils.get_expected_device_object_rtb23(), True
    )
    assert bid_request_validator.is_user_as_expected(brUtils.get_expected_user_object())
    assert bid_request_validator.is_ext_object_as_expected(
        brUtils.get_expected_ext_object(root_domain)
    )


@description(
    "PII is hidden from bid requests v2.4 when sharing opt notice not provided and not opted out"
)
@pytest.mark.regression
def test_bid_request_ctv_gpp_sharing_opt_out_true_notice_2_optout_2_rtb24():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_gpp_sharing_opt_out_true_notice_2_optout_2_rtb24"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.gpp = "DBABLA~BCAIAAAAAAA.QA"  # Notice = 2 OptOut = 2
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_gpp_sharing_opt_out_true_notice_2_optout_2_rtb24"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    assert bid_request_validator.is_device_object_as_expected(
        brUtils.get_expected_device_object_rtb24(), True
    )
    assert bid_request_validator.is_user_as_expected(brUtils.get_expected_user_object())
    assert bid_request_validator.is_ext_object_as_expected(
        brUtils.get_expected_ext_object(root_domain)
    )
