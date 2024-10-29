import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the app ver is present in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_app_ver():
    case = Case("test_app_ver")  # This is the file to test this case

    vpc = case.vpc
    vpc.app_ver = "1.2.1"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["app_ver=" + vpc.app_ver])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
