import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the content title is present in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_content_title():
    case = Case("test_content_title")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_title = "Star Wars"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["content_title=" + vpc.content_title])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
