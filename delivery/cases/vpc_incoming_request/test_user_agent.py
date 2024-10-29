import pytest
from core.case import Case
from core.devices import DEVICE_CTV_ROKU
from core.vastValidator import VastValidator


# This would test that user-agent is correctly populated in vpc incoming request in delivery logs.
@pytest.mark.regression
def test_user_agent_query_parameter():
    case = Case("test_user_agent_query_parameter")  # This is the file to test this case

    vpc = case.vpc
    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery([vpc.ua])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


# This would test that when ua value is empty user-agent is  populated in header userAgent in vpc incoming request in
# delivery logs.
@pytest.mark.regression
def test_user_agent_header():
    case = Case("test_user_agent_header")  # This is the file to test this case

    vpc = case.vpc
    case.logDelivery = "userAgent=python-requests"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["userAgent=python-requests"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
