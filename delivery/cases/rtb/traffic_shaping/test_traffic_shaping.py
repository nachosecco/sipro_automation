import logging

import pytest
from core.Description import description
from core.dto.event import EventType, Event
from core.traffic_shaping import TrafficShaping
from core.vastValidator import VastValidator

from core.case import Case


@pytest.mark.regression
@description(
    "Test that a bidder blocked by traffic shaping is only called ~5 percent of the time"
)
def test_traffic_shaping_bidder_is_blocked():
    case = Case("test_traffic_shaping_bidder_is_blocked")
    vpc = case.vpc
    vpc.app_id = "test_traffic_shaping_bidder_is_blocked"

    traffic_shaping = TrafficShaping()
    blocked_bidders_guids = traffic_shaping.load_blocked_bidders_cache(
        vpc, ["test_traffic_shaping_bidder_is_blocked"]
    )

    event = Event()
    event.event_type = EventType.RTB_EVENT
    event.blocked_bidders_guids = blocked_bidders_guids

    num_blocked_bidders_allowed_through = 0
    have_asserted_rtb_event = False

    for _ in range(100):
        vpc.regenerate_automation_framework()
        vast_result = VastValidator().test(vpc)

        try:
            vast_result.assert_vast_xml().assert_ad_count(0)

            # This is a time consuming assertion, so we only want to do it once
            if not have_asserted_rtb_event:
                vast_result.assert_event().assert_expected_event_in_the_log(event)
                have_asserted_rtb_event = True
        except AssertionError:
            vast_result.assert_vast_xml().assert_ad_count(1)
            num_blocked_bidders_allowed_through += 1

    if (
        num_blocked_bidders_allowed_through < 2
        or num_blocked_bidders_allowed_through > 8
    ):
        logging.error(
            f"The total number of blocked bidders allowed through ({num_blocked_bidders_allowed_through}) is outside of the expected probability range of ~5% "
            "(we are using [2, 8] for a sample size of 100)."
        )
        assert False
