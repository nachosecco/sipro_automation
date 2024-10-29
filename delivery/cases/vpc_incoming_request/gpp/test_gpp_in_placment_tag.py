import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.constants import REPLACE


# This would test that the gpp parameter value sent is present in delivery logs.
@pytest.mark.regression
def test_gpp_param():
    # Configuration includes a placement without a media aligned
    case = Case("test_gpp_param")
    vpc = case.vpc
    vpc.gpp = "BBC"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery([f"gpp={vpc.gpp}"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


# This would test that the gpp parameter has default value in delivery logs.
@pytest.mark.regression
def test_missing_gpp_param():
    # Configuration includes a placement without a media aligned
    case = Case("test_missing_gpp_param")

    vpc = case.vpc

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery([f"gpp={REPLACE}"])
