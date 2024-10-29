import pytest
from core.Description import description
from core.case import Case
from core.dto.event import EventType
from core.vastValidator import VastValidator


@description("Test that the content qagmediarating is present in delivery logs")
@pytest.mark.regression
@pytest.mark.smoke
def test_content_qagmediarating():
    case = Case("test_content_qagmediarating")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_qagmediarating = "2"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    vast_result.assert_logs_delivery(["content_qagmediarating=2"])

    # This will execute the all assertions in the case
    vast_result.assert_case(case)


@description(
    "Content qagmediarating input generates expected values in the kafka event"
)
@pytest.mark.regression
@pytest.mark.smoke
def test_content_qagmediarating_event_values():
    case = Case("test_content_qagmediarating_event_values")
    vpc = case.vpc
    # Given a content_qagmediarating value of '1' the event should be ALL_AUDIENCES
    assert_case_and_mediarating_event(
        case, vpc, "1", expected_event_media_rating="ALL_AUDIENCES"
    )
    # Given a content_qagmediarating value of '2' the event should be EVERYONE_OVER_12
    assert_case_and_mediarating_event(
        case, vpc, "2", expected_event_media_rating="EVERYONE_OVER_12"
    )
    # Given a content_qagmediarating value of '3' the event should be MATURE_AUDIENCES
    assert_case_and_mediarating_event(
        case, vpc, "3", expected_event_media_rating="MATURE_AUDIENCES"
    )

    # Given a content_qagmediarating value of '0' the value should be ignored
    # and the log should contain a parse warning
    vast_result = assert_case_and_mediarating_event(
        case, vpc, "0", expected_event_media_rating=""
    )
    vast_result.assert_logs_delivery("Failed to parse MediaRating from 0")

    # Given a content_qagmediarating value of 'TV-18' the value should be ignored
    # and the log should contain a parse warning
    vast_result = assert_case_and_mediarating_event(
        case, vpc, "TV-18", expected_event_media_rating=""
    )
    vast_result.assert_logs_delivery("Failed to parse MediaRating from TV-18")


def assert_case_and_mediarating_event(
    case, vpc, vpc_content_qagmediarating, expected_event_media_rating
):
    # Generate a new automation framework id
    vpc.regenerate_automation_framework()
    vpc.content_qagmediarating = vpc_content_qagmediarating
    # Execute the framework
    vast_result = VastValidator().test(vpc)
    # Execute all assertions in the case
    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.VIDEOTRUEFIRSTCALL
    event.beacon_event_type = EventType.VIDEOTRUEFIRSTCALL.name
    event.mediaRating = expected_event_media_rating

    # Execute the assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    # Return this in case additional assertions are needed
    return vast_result
