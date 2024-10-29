import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the content genre is present in delivery logs.
@pytest.mark.regression
def test_content_genre():
    case = Case("test_content_genre")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_genre = "Comedy, Drama"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["content_genre=Comedy, Drama"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
