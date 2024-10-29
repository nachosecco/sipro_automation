import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    """Test delivery adpod media count 3 and returns 2 where_pod_max_ad_dur is 15 sec and_ad_max_dur is 60 sec"""
)
def test_delivery_pod_automation_where_pod_max_ad_dur_15_and_ad_max_dur_60():
    case = Case(
        "test_delivery_pod_automation_where_pod_max_ad_dur_15_and_ad_max_dur_60"
    )

    """
	Select a placement aligned with 3 medias
	1. Asset media with 15 sec
	2. Asset media with 15 sec
	3. RTB with 30 sec
	Result: the 2 media should be in the pod and RTB should be out side of the pod
	"""
    vpc = case.vpc
    vpc.pod_max_dur = "60"
    vpc.pod_max_ad_dur = "15"

    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)

    expectedAdPod = case.adPod
    expectedAdPod.pod_size = 2
    assert vastResult.assertAdPod().isVastHasTheExpectedPod(expectedAdPod)
    vastResult.assertXML().assertAdsCount(2)


@pytest.mark.regression
@description(
    """Test delivery adpod media count 3 and returns 3 where_pod_max_ad_dur is 15 sec and_ad_max_dur is 60 sec"""
)
def test_delivery_pod_automation_where_pod_max_ad_dur_15_and_ad_max_dur_60_2():
    case = Case(
        "test_delivery_pod_automation_where_pod_max_ad_dur_15_and_ad_max_dur_60_2"
    )
    """
	Select a placement aligned with 3 medias
	1. Asset media with 15 sec
	2. Asset media with 15 sec
	3. Asset media with 15 sec
	Result: All 3 media should be inside the pod
	"""
    vpc = case.vpc
    vpc.pod_max_dur = "60"
    vpc.pod_max_ad_dur = "15"

    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)

    expectedAdPod = case.adPod
    expectedAdPod.pod_size = 3
    assert vastResult.assertAdPod().isVastHasTheExpectedPod(expectedAdPod)

    vastResult.assertXML().assertAdsCount(3)
