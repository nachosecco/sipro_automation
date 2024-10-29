import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the content series is present in delivery logs.
@pytest.mark.regression
def test_content_series():
    case = Case("test_content_series")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_series = "The Office"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["content_series=" + vpc.content_series])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)