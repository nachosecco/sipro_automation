import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the content prodq is present in delivery logs.
@pytest.mark.regression
def test_content_prodq():
    case = Case("test_content_prodq")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_prodq = "1"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["content_prodq=1"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
