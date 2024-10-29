import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the content episode is present in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_content_episode():
    case = Case("test_content_episode")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_episode = "5"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["content_episode=" + vpc.content_episode])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
