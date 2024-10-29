import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_adpod_pod_min_dur_15():
    case = Case("test_media_adpod_pod_min_dur_15")

    vpc = case.vpc
    vpc.pod_min_ad_dur = "15"
    vpc.pod_size = "2"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 1
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(2)
