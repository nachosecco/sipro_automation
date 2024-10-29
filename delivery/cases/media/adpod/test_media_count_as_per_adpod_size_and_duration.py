import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_got_all_3_media_as_per_adpod_size_and_duration():
    case = Case("test_got_all_3_media_as_per_adpod_size_and_duration")

    vpc = case.vpc
    vpc.pod_size = "3"
    vpc.pod_max_dur = "60"
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 3
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
def test_got_two_filtered_media_as_per_adpod_size_and_duration():
    case = Case("test_got_two_filtered_media_as_per_adpod_size_and_duration")

    vpc = case.vpc
    vpc.pod_size = "3"
    vpc.pod_max_dur = "60"
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 2
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
def test_got_one_filtered_media_as_per_adpod_size_and_duration():
    case = Case("test_got_one_filtered_media_as_per_adpod_size_and_duration")

    vpc = case.vpc
    vpc.pod_size = "3"
    vpc.pod_max_dur = "60"
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 1
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)
