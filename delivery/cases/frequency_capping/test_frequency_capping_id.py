import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the app id is present in delivery logs.
@pytest.mark.regression
def test_frequency_capping_device_id_0000():
    # The campaing align to this placement to this case, is important that have frequency capping on
    case = Case(
        "test_frequency_capping_device_id_0000"
    )  # This is the file to test this case

    vpc = case.vpc

    # This is a very specific case to test, the session id created in delivery and reuse in event
    vpc.did = "00000000-0000-0000-0000-000000000000"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery(["sessionUUID=true"])

    vastResult.assertXML().assertTagImpressionContainsText("cid_tsi=1")
