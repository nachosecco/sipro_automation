import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the app name is present in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_app_name():
    case = Case("test_app_name")  # This is the file to test this case

    vpc = case.vpc
    vpc.app_name = "Roku"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["app_name=" + vpc.app_name])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


# This would test blocked app name.
def test_blocked_app_name():
    case = Case("test_blocked_app_name")  # This is the file to test this case

    vpc = case.vpc
    vpc.app_name = "adultdreams"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will assert that value is passed
    vastResult.assertLogsDelivery(["app_name=adultdreams"])
