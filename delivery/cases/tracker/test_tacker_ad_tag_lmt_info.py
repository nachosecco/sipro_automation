import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_delivery_automation_tracker_info_lmt_pass_values_1():
    case = Case("test_delivery_automation_tracker_info_lmt_pass_values_1")
    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.lmt = "1"
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    assert_tracker_tags = vast_result.assertXML().assertTrackerTags(
        "deliverylmttracker.com"
    )
    assert_tracker_tags.ad_tag("lmt", vpc.lmt)
    assert_tracker_tags.ad_tag("device_id", "")
    vast_result.assertLogsDelivery(["lmt=1"])


@pytest.mark.regression
def test_delivery_automation_tracker_info_lmt_pass_values_0():
    case = Case("test_delivery_automation_tracker_info_lmt_pass_values_0")
    vpc = case.vpc
    vpc.lmt = "0"
    vpc.did = "3824add4-6141-5a8b-9b85-d88c2ff781b1"
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_tracker_tags = vast_result.assertXML().assertTrackerTags(
        "deliverylmttracker.com"
    )
    assert_tracker_tags.ad_tag("lmt", vpc.lmt)
    assert_tracker_tags.ad_tag("device_id", vpc.did)
    vast_result.assertLogsDelivery(["lmt=0"])


@pytest.mark.regression
def test_delivery_automation_tracker_info_lmt_pass_invalid_values_11():
    case = Case("test_delivery_automation_tracker_info_lmt_pass_invalid_values_11")
    vpc = case.vpc
    vpc.lmt = "11"
    vpc.did = "3824add4-6141-5a8b-9b85-d88c2ff781b1"
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    assert_tracker_tags = vast_result.assertXML().assertTrackerTags(
        "deliverylmttracker.com"
    )
    assert_tracker_tags.ad_tag("lmt", "0")
    assert_tracker_tags.ad_tag("device_id", vpc.did)
    vast_result.assertLogsDelivery(["lmt=11"])
