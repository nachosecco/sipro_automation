import core.utils.piiBidRequestUtils as brUtils
import pytest
from core.case import Case
from core.configuration import Configuration
from core.enums.gppSection import GPPSection

from core.Description import description
from core.utils.geoIpUtils import get_ip_for_geo
from core.vastValidator import VastValidator


@description(
    "Test bid request v2.6 don't have geo and other pii info when known child sensitive data consents is provided as "
    "1,1"
)
@pytest.mark.regression
def test_bid_request_gpp_known_child_sensitive_data_consents_true_1_1_rtb26():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_1_1_rtb26"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABLA~BAAAAAAAUAA.QA"
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
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_1_1_rtb26"
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
    "Test bid request from virginia v2.6 don't have geo and other pii info when known child sensitive data consents is provided as "
    "1"
)
@pytest.mark.regression
def test_bid_request_colorado_gpp_known_child_sensitive_data_consents_true_1_rtb26():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_colorado_gpp_known_child_sensitive_data_consents_true_1_rtb26"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.gpp = "DBABJg~BAAAAQA.QA"  # Colorado, consent 1
    vpc.gpp_sid = GPPSection.COLORADO.id
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_colorado_gpp_known_child_sensitive_data_consents_true_1_rtb26"
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
    "Test bid request v2.5 don't have geo and other pii info when known child sensitive data consents is provided as "
    "1,2"
)
@pytest.mark.regression
def test_bid_request_gpp_known_child_sensitive_data_consents_true_1_2_rtb25():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_1_2_rtb25"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABLA~BAAAAAAAYAA.QA"
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
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_1_2_rtb25"
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
    "Test bid request v2.5 from Utah don't have geo and other pii info when known child sensitive data consents is provided as "
    "1"
)
@pytest.mark.regression
def test_bid_request_utah_gpp_known_child_sensitive_data_consents_true_1_rtb25():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_utah_gpp_known_child_sensitive_data_consents_true_1_rtb25"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABFg~BAAAABAA"  # Utah, consent is 1
    vpc.gpp_sid = GPPSection.UTAH.id
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Utah")
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_utah_gpp_known_child_sensitive_data_consents_true_1_rtb25"
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
    "Test bid request v2.3 don't have geo and other pii info when known child sensitive data consents is provided as "
    "1,0"
)
@pytest.mark.regression
def test_bid_request_gpp_known_child_sensitive_data_consents_true_1_0_rtb23():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_1_0_rtb23"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABLA~BAAAAAAAQAA.QA"
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
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_1_0_rtb23"
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
    "Test bid request v2.4 don't have geo and other pii info when known child sensitive data consents is provided as "
    "2,1"
)
# Test RTB 2.4 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_gpp_known_child_sensitive_data_consents_true_2_1_rtb24():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_2_1_rtb24"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.gpp = "DBABLA~BAAAAAAAkAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.ip_address = get_ip_for_geo(country="US", region="Connecticut")
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_2_1_rtb24"
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


@description(
    "Test bid request v2.2 don't have geo and other pii info when known child sensitive data consents is provided as "
    "0,1"
)
@pytest.mark.regression
def test_bid_request_gpp_known_child_sensitive_data_consents_true_0_1_rtb22():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_0_1_rtb22"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABLA~BAAAAAAAEAA.QA"
    vpc.gpp_sid = GPPSection.US_NATIONAL.id
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Virginia")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_gpp_known_child_sensitive_data_consents_true_0_1_rtb22"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    brUtils.validate_rtb_ctv_common_properties(bid_request_validator)
    assert bid_request_validator.is_device_object_as_expected(
        brUtils.get_expected_device_object_rtb22(), True
    )
    assert bid_request_validator.is_user_as_expected(brUtils.get_expected_user_object())
    assert bid_request_validator.is_ext_object_as_expected(
        brUtils.get_expected_ext_object(root_domain)
    )
