import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_adpod_with_pod_max_dur_15_media_10s():
    case = Case("test_media_adpod_with_pod_max_dur_15_media_10s")

    vpc = case.vpc
    vpc.pod_max_ad_dur = "15"
    vpc.pod_size = "2"

    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)

    expectedAdPod = case.adPod
    expectedAdPod.pod_size = 1
    assert vastResult.assertAdPod().isVastHasTheExpectedPod(expectedAdPod)

    vastResult.assertXML().assertAdsCount(2)


@pytest.mark.regression
def test_media_adpod_with_pod_max_dur_30_media_30s():
    case = Case("test_media_adpod_with_pod_max_dur_30_media_30s")

    vpc = case.vpc
    vpc.pod_max_ad_dur = "30"
    vpc.pod_size = "2"

    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)

    expectedAdPod = case.adPod
    expectedAdPod.pod_size = 2
    assert vastResult.assertAdPod().isVastHasTheExpectedPod(expectedAdPod)

    vastResult.assertXML().assertAdsCount(2)
