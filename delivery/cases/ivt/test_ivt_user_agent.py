import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.ivt import IVT


@pytest.mark.regression
def test_ivt_user_agent_invalid():
    case = Case("test_ivt_user_agent_invalid")

    vpc = case.vpc
    vpc.ua = "CustomPlayer1/3 (iOS 12.4.9; Other; Proxy)"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.user_agent == vpc.ua

    # Assert Results
    assert ivt.response.is_passed == "false"
    assert ivt.response.checks.user_agent.result == "MEETS_THRESHOLD"
    assert ivt.response.did_not_pass_category == "USER_AGENT"

    vast_result.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_ivt_user_agent_valid():
    case = Case("test_ivt_user_agent_valid")

    vpc = case.vpc
    vpc.ua = "Roku4640X/DVP-7.70 (297.70E04154A)"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.user_agent == vpc.ua

    # Assert Results
    assert ivt.response.is_passed == "true"
    assert ivt.response.did_not_pass_category == ""

    vast_result.assertXML().assertAdsCount(1)
