import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_adpod_with_pod_max_dur_90_media_15s():
    case = Case("test_media_adpod_with_pod_max_dur_90_media_15s")

    vpc = case.vpc
    vpc.pod_max_dur = "90"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 4
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assertXML().assertAdsCount(4)


@pytest.mark.regression
def test_media_adpod_with_pod_max_dur_90_media_30s():
    case = Case("test_media_adpod_with_pod_max_dur_90_media_30s")

    vpc = case.vpc
    vpc.pod_max_dur = "90"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 3
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assertXML().assertAdsCount(4)


@pytest.mark.regression
def test_media_adpod_with_pod_max_dur_90_media_35s():
    case = Case("test_media_adpod_with_pod_max_dur_90_media_35s")

    vpc = case.vpc
    vpc.pod_max_dur = "90"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 2
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assertXML().assertAdsCount(4)
