import pytest
from core.case import Case

from core.vastValidator import VastValidator
from core.dto.event import EventType


# This would test whether event sent for a demand opportunity are expected.
@pytest.mark.regression
def test_delivery_automation_opportunity_event_ip_address():
    case = Case("test_delivery_automation_opportunity_event_ip_address")
    vpc = case.vpc
    vpc.ip_address = "174.216.245.107"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.VIDEOTRUEFIRSTCALL

    event.ipAddressOverride = vpc.ip_address

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_delivery_automation_rtb_event_ip_address():
    case = Case("test_delivery_automation_rtb_event_ip_address")
    vpc = case.vpc
    vpc.ip_address = "174.216.245.107"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.RTB_EVENT

    event.ipAddressOverride = vpc.ip_address

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)
