import pytest

from core.Description import description
from core.case import Case
from core.dto.event import EventType
from core.vastValidator import VastValidator


@description("This would test that the content livestream is present in delivery logs.")
@pytest.mark.regression
@pytest.mark.smoke
def test_content_livestream():
    case = Case("test_content_livestream")
    vpc = case.vpc
    vpc.content_livestream = "0"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    vast_result.assert_logs_delivery(["content_livestream=0"])

    # This will execute the all assertions in the case
    vast_result.assert_case(case)


@description(
    "This would test that the content with incoming value [true,yes,1,false,no,0] livestream"
    " and check is present in kafka event with yes or no"
)
@pytest.mark.regression
@pytest.mark.smoke
def test_content_livestream_event_values():
    case = Case("test_content_livestream_event_values")
    vpc = case.vpc
    # Testing with true value it should have yes value

    content_value_check_for(case, vpc, "true", event_live_stream="YES")

    # Testing with yes value it should have yes value

    content_value_check_for(case, vpc, "yes", event_live_stream="YES")

    # Testing with 1 value it should have yes value

    content_value_check_for(case, vpc, "1", event_live_stream="YES")

    # Testing with false value it should have no value

    content_value_check_for(case, vpc, "false", event_live_stream="NO")

    # Testing with 0 value it should have no value

    content_value_check_for(case, vpc, "no", event_live_stream="NO")

    # Testing with 0 value it should have no value

    content_value_check_for(case, vpc, "0", event_live_stream="NO")


def content_value_check_for(case, vpc, vpc_content_livestream, event_live_stream):
    vpc.regenerate_automation_framework()

    vpc.content_livestream = vpc_content_livestream
    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    # This will execute the all assertions in the case
    vast_result.assert_case(case)
    event = case.event
    event.event_type = EventType.VIDEOTRUEFIRSTCALL
    event.beacon_event_type = EventType.VIDEOTRUEFIRSTCALL.name
    event.liveStream = event_live_stream

    vast_result.assert_event().assert_expected_event_in_the_log(event)
