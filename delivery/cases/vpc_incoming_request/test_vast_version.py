import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_vast_version_2_0():
    case = Case("test_vast_version_2_0")
    vpc = case.vpc

    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)
    vastResult.assertXML().assertVastVersion("2.0")


@pytest.mark.regression
def test_vast_version_3_0():
    case = Case("test_vast_version_3_0")
    vpc = case.vpc

    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)
    vastResult.assertXML().assertVastVersion("3.0")


@pytest.mark.regression
def test_vast_version_4_0():
    case = Case("test_vast_version_4_0")
    vpc = case.vpc

    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)
    vastResult.assertXML().assertVastVersion("4.0")
