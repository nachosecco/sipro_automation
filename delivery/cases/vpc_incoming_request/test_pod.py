import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.Description import description


# This would test that pod_max_ad_dur is correctly populated in vpc incoming request in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_pod_max_ad_dur_60_sec():
    case = Case("test_pod_max_ad_dur_60_sec")  # This is the file to test this case

    vpc = case.vpc
    vpc.pod_max_ad_dur = "60"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # This will asssert that the value is passed
    vastResult.assertLogsDelivery(["pod_max_ad_dur=60"])


# This would test that pod_max_dur is correctly populated in vpc incoming request in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_pod_max_dur():
    case = Case("test_pod_max_dur")  # This is the file to test this case

    vpc = case.vpc
    vpc.pod_max_dur = "30"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # This will asssert that the value is passed
    vastResult.assertLogsDelivery(["pod_max_dur=30"])


# This would test that pod_min_ad_dur is correctly populated in vpc incoming request in delivery logs.
@pytest.mark.regression
def test_pod_min_ad_dur():
    case = Case("test_pod_min_ad_dur")  # This is the file to test this case

    vpc = case.vpc
    vpc.pod_min_ad_dur = "5"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # This will asssert that the value is passed
    vastResult.assertLogsDelivery(["pod_min_ad_dur=5"])


@pytest.mark.regression
@description(
    """This would test that wrapper ad still gets served for pod request considering the default time.
    Configuration : Placement has one programmatic demand with bidder configured to return the wrapper ad response"""
)
def test_wrapper_pod_dur():
    case = Case("test_wrapper_pod_dur")  # This is the file to test this case
    vpc = case.vpc
    vpc.pod_min_ad_dur = "5"
    vpc.pod_max_ad_dur = "30"
    vpc.pod_size = "1"
    vpc.pod_max_dur = "30"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assert_vast_xml().assert_ad_count(1)

    # This instance has the information of assertion of adPod
    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 1

    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)


@pytest.mark.regression
@description(
    """This would test that wrapper ad gets filtered for pod request considering the default
duration is greater than pod max duration
Configuration : Placement has one programmatic demand with bidder configured to return the wrapper ad response.
"""
)
def test_wrapper_pod_dur_lower_than_default():
    case = Case(
        "test_wrapper_pod_dur_lower_than_default"
    )  # This is the file to test this case
    vpc = case.vpc
    vpc.pod_min_ad_dur = "5"
    vpc.pod_max_ad_dur = "20"
    vpc.pod_size = "1"
    vpc.pod_max_dur = "20"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 0
    # This would assert that is only one ad in the vast xml
    vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)
