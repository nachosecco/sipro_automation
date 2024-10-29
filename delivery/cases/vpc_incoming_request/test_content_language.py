import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the content language is present in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_content_language():
    case = Case("test_content_language")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_language = "eng"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["content_language=eng"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
