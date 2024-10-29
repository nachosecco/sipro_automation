import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_adpod_pod_min_ad_dur_30_and_ad_max_dur_60_return_30():
    case = Case(
        "test_media_adpod_pod_min_ad_dur_15_pod_max_ad_dur_30_and_ad_max_dur_120"
    )

    vpc = case.vpc
    vpc.pod_min_ad_dur = "15"
    vpc.pod_max_ad_dur = "30"
    vpc.pod_max_dur = "120"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    expected_ad_pod = case.adPod
    expected_ad_pod.pod_size = 4
    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    vast_result.assert_vast_xml().assert_ad_count(6)
