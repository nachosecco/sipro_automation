import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_delivery_automation_max_pod_size_5_with_5_media_return_in_the_pod():
    case = Case(
        "test_delivery_automation_max_pod_size_5_with_5_media_return_in_the_pod"
    )

    vpc = case.vpc
    vpc.pod_size = "5"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 5
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(5)


@pytest.mark.regression
def test_delivery_automation_max_pod_size_5_with_5_media_in_pod_1_in_vast():
    case = Case("test_delivery_automation_max_pod_size_5_with_5_media_in_pod_1_in_vast")

    vpc = case.vpc
    vpc.pod_size = "5"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 5
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(6)
