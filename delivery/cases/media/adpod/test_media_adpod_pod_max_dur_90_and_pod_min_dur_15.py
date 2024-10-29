import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_adpod_pod_max_dur_90_and_ad_min_dur_15s():
    case = Case("test_media_adpod_pod_max_dur_90_and_ad_min_dur_15s")

    vpc = case.vpc
    vpc.pod_max_dur = "90"
    vpc.pod_min_ad_dur = "15"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 6
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)
    vast_result.assert_vast_xml().assert_ad_count(6)


@pytest.mark.regression
def test_media_adpod_pod_max_dur_90_and_ad_min_dur_15_30s():
    case = Case("test_media_adpod_pod_max_dur_90_and_ad_min_dur_15_30s")

    vpc = case.vpc
    vpc.pod_max_dur = "90"
    vpc.pod_min_ad_dur = "15"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 3
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(6)


@pytest.mark.regression
def test_media_adpod_pod_max_ad_dur_90_and_min_ad_dur_15_4m():
    case = Case("test_media_adpod_pod_max_ad_dur_90_and_min_ad_dur_15_4m")

    vpc = case.vpc
    vpc.pod_max_dur = "90"
    vpc.pod_min_ad_dur = "15"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 4
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(6)
