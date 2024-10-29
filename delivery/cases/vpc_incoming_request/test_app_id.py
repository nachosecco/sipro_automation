import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the app id is present in delivery logs.
@pytest.mark.regression
def test_app_id():
    case = Case("test_app_id")  # This is the file to test this case

    vpc = case.vpc
    vpc.app_id = "com.apple.mobilesafari"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["app_id=" + vpc.app_id])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


# This would test that the app id is mandatory.
def test_missing_app_id():
    case = Case("test_missing_app_id")  # This is the file to test this case

    vpc = case.vpc
    vpc.app_id = ""

    # This would execute the framework
    vastResult = VastValidator().test(vpc, 400)

    # Extra assertions for this case
    vastResult.assertCase(case)
