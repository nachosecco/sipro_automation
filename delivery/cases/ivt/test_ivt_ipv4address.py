import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.ivt import IVT


@pytest.mark.regression
def test_ivt_ipv4address_valid():
    case = Case("test_ivt_ipv4address_valid")

    vpc = case.vpc
    vpc.ip_address = "52.13.119.116"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.ip == vpc.ip_address

    # Assert Results
    assert ivt.response.is_passed == "true"
    assert ivt.response.did_not_pass_category == ""

    vast_result.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_ivt_ipv4address_invalid():
    case = Case("test_ivt_ipv4address_invalid")

    vpc = case.vpc
    vpc.ip_address = "47.219.204.103"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.ip == vpc.ip_address

    # Assert Results
    assert ivt.response.is_passed == "false"
    assert ivt.response.checks.ip_v4.result == "MEETS_THRESHOLD"
    assert ivt.response.did_not_pass_category == "IP"

    vast_result.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_ivt_ipv4address_threshold_valid():
    case = Case("test_ivt_ipv4address_threshold_valid")

    vpc = case.vpc
    vpc.ip_address = "153.187.96.213"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.ip == vpc.ip_address

    # Assert Results
    assert ivt.response.is_passed == "true"
    assert ivt.response.did_not_pass_category == ""
    assert ivt.response.checks.ip_v4.result == "PASSED_UNDER_THRESHOLD"

    vast_result.assertXML().assertAdsCount(1)
