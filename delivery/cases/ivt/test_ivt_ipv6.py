import pytest

from core.case import Case
from core.vastValidator import VastValidator
from core.ivt import IVT


@pytest.mark.regression
def test_ivt_ipv6_blocked():
    case = Case("test_ivt_ipv6_blocked")

    vpc = case.vpc
    vpc.ip_address = "2607:fb90:ae1f:d04:0:3:997c:a001"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.ip == vpc.ip_address

    # Assert Results
    assert ivt.response.is_passed == "false"
    assert ivt.response.checks.ip_v6.result == "MEETS_THRESHOLD"
    assert ivt.response.did_not_pass_category == "IP"

    vast_result.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_ivt_ipv6_valid():
    case = Case("test_ivt_ipv6_valid")

    vpc = case.vpc
    vpc.ip_address = "2605:6440:4000:1000:0:0:0:bf5a"

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
def test_ivt_ipv6_valid_belowthreshhold():
    case = Case("test_ivt_ipv6_valid_belowthreshhold")

    vpc = case.vpc
    vpc.ip_address = "2607:fb90:2ac:484:9a:8c7c:ca1d:b330"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.ip == vpc.ip_address

    # Assert Results
    assert ivt.response.is_passed == "true"
    assert ivt.response.did_not_pass_category == ""
    assert ivt.response.checks.ip_v6.result == "PASSED_UNDER_THRESHOLD"

    vast_result.assertXML().assertAdsCount(1)
