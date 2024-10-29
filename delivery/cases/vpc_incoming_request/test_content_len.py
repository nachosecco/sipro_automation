import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the content len is present in delivery logs.
@pytest.mark.regression
def test_content_len():
    case = Case("test_content_len")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_len = "180"
    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["content_len=180"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


# This would test invalid content len.
def test_invalid_content_len():
    case = Case("test_invalid_content_len")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_len = "Testing"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will assert that value is passed
    vastResult.assertLogsDelivery(["content_len=Testing"])
