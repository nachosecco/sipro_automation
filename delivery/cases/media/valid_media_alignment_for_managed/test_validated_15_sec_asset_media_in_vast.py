import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test a placement that exists and check that is ok.
@pytest.mark.regression
def test_validated_15_sec_asset_media_duration():
    case = Case(
        "test_validated_15_sec_asset_media_duration"
    )  # This is the file to test this case

    vpc = case.vpc
    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    vastResult.assertXML().assertDuration("00:00:15")
    vastResult.assertLogsDelivery(["1 valid media post filters", "passed all filters"])

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)
