import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_adpod_without_any_pod_tag():
    case = Case("test_media_adpod_without_any_pod_tag")

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 0
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
def test_media_adpod_missing_required_pod_tag():
    case = Case("test_media_adpod_missing_required_pod_tag")

    vpc = case.vpc
    vpc.pod_max_ad_dur = "30"
    vpc.pod_min_ad_dur = "5"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 0
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
def test_media_adpod_with_only_pod_max_dur():
    case = Case("test_media_adpod_with_only_pod_max_dur")

    vpc = case.vpc
    vpc.pod_max_dur = "60"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 3
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
def test_media_adpod_with_only_pod_size():
    case = Case("test_media_adpod_with_only_pod_size")

    vpc = case.vpc
    vpc.pod_size = "2"
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)
    vast_result.assertLogsDelivery("pod_size=2")

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 2
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(3)
