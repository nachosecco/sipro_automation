import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the app uri is present in delivery logs.
@pytest.mark.regression
def test_app_uri():
    case = Case("test_app_uri")  # This is the file to test this case

    vpc = case.vpc
    vpc.app_uri = "http://itunes.apple.com"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["app_uri=" + vpc.app_uri])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
