import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_adpod_vast_version_3_supported():
    case = Case("test_media_adpod_vast_version_3_supported")

    vpc = case.vpc
    vpc.pod_size = "2"
    vpc.pod_max_dur = "30"
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)
    vast_result.assertLogsDelivery(["pod_size=2"])

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 2
    expected_ad_pod.ads_size_in_vast = 3
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
def test_media_adpod_vast_version_4_supported():
    case = Case("test_media_adpod_vast_version_4_supported")

    vpc = case.vpc
    vpc.pod_size = "2"
    vpc.pod_max_dur = "30"
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)
    vast_result.assertLogsDelivery(["pod_size=2"])
    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 2
    expected_ad_pod.ads_size_in_vast = 3

    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
def test_media_adpod_vast_version_2_not_supported():
    case = Case("test_media_adpod_vast_version_2_not_supported")

    vpc = case.vpc
    vpc.pod_size = "2"
    vpc.pod_max_dur = "30"
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)
    vast_result.assertLogsDelivery(["pod_size=2"])

    expected_ad_pod = case.adPod

    # since vast version is 2 this would be 0
    expected_ad_pod.pod_size = 0
    expected_ad_pod.ads_size_in_vast = 3

    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)
