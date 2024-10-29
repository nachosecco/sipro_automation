import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator
from core.dto.event import EventType


@description("This will test that the incoming schain value is in opportunity event")
@pytest.mark.regression
def test_opportunity_event_schain():
    case = Case("test_opportunity_event_schain")
    vpc = case.vpc
    vpc.schain = "1.0,1!example.tv,973016,1,,,"

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    event = case.event
    event.event_type = EventType.VIDEOTRUEFIRSTCALL
    event.beacon_event_type = EventType.VIDEOTRUEFIRSTCALL.name
    event.schain = vpc.schain

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)
