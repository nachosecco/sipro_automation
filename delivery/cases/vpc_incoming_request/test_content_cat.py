import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the content cat is present in delivery logs.
@pytest.mark.regression
def test_content_cat():
    case = Case("test_content_cat")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_cat = "IAB1-7"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["content_cat=IAB1-7"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


# This would test invalid content cat.
def test_invalid_content_cat():
    case = Case("test_invalid_content_cat")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_cat = "Testing"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will assert that value is passed
    vastResult.assertLogsDelivery(["content_cat=Testing"])
