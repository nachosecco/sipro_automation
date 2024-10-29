import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that the addpod is 1 by duration.
@pytest.mark.regression
def test_media_adpod_max_ads_1_by_duration():
    case = Case("test_media_adpod_max_ads_1_by_duration")

    vpc = case.vpc
    vpc.pod_max_dur = "7"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This instance has the information of assertion of adPod
    expected_ad_pod = case.adPod

    # This would override information in data file
    expected_ad_pod.pod_size = 1

    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    # This would assert there is only one ad in the vast xml
    vast_result.assertXML().assert_ad_count(3)


# This would test that the addpod is 1 by size.
@pytest.mark.regression
def test_media_adpod_max_ads_1_by_size():
    case = Case("test_media_adpod_max_ads_1_by_size")

    vpc = case.vpc
    vpc.pod_size = "1"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This instance has the information of assertion of adPod
    expected_ad_pod = case.adPod

    # This would override information in data file
    expected_ad_pod.pod_size = 1

    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assert_ad_count(3)


# This would test that the addpod is 1 and max duration.
@pytest.mark.regression
def test_media_adpod_max_ads_1_by_ad_max_duration():
    case = Case("test_media_adpod_max_ads_1_by_ad_max_duration")

    vpc = case.vpc
    vpc.pod_max_dur = "7"
    vpc.pod_max_ad_dur = "7"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This instance has the information of assertion of adPod
    expected_ad_pod = case.adPod

    # This would override information in data file
    expected_ad_pod.pod_size = 1

    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assert_ad_count(3)


# This would test that the addpod is 1.
@pytest.mark.regression
def test_media_adpod_max_ads_1_by_ad_min_duration():
    case = Case("test_media_adpod_max_ads_1_by_ad_min_duration")

    vpc = case.vpc
    vpc.pod_max_dur = "61"
    vpc.pod_min_ad_dur = "50"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This instance has the information of assertion of adPod
    expected_ad_pod = case.adPod

    # This would override information in data file
    expected_ad_pod.pod_size = 1

    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assert_ad_count(3)


# This would test that the addpod is 0 and min duration.
@pytest.mark.regression
def test_media_adpod_is_ads_0_by_ad_min_duration():
    case = Case("test_media_adpod_is_ads_0_by_ad_min_duration")
    # vpc_pod_max_ad_dur,vpc_pod_max_dur
    vpc = case.vpc

    vpc.pod_max_ad_dur = "3"
    vpc.pod_max_dur = "61"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This instance has the information of assertion of adPod
    expected_ad_pod = case.adPod

    # This would override information in data file
    expected_ad_pod.pod_size = 0

    assert vast_result.assertAdPod().isVastHasTheExpectedPod(expected_ad_pod)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assert_ad_count(3)
