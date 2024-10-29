import pytest
from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description(
    "This would test that ssai is correctly populated in vpc incoming request in delivery logs."
)
@pytest.mark.regression
@pytest.mark.smoke
def test_valid_ssai():
    case = Case("test_valid_ssai")

    vpc = case.vpc
    vpc.ssai = "2"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["ssai=2"])

    # This will execute the all assertions in the case
    vastResult.assert_case(case)


@description(
    "This would test that ssai is populated as ZERO for invalid value in vpc incoming request in delivery logs."
)
@pytest.mark.regression
@pytest.mark.smoke
def test_invalid_ssai():
    case = Case("test_invalid_ssai")

    vpc = case.vpc
    vpc.ssai = "20"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["ssai=0"])

    # This will execute the all assertions in the case
    vastResult.assert_case(case)
