import pytest

from core.Description import description
from core.case import Case
from core.contentInfo import (
    content_catagory_IAB_1,
    qagmediarating_1,
    livestream_1,
    ProductionQuality_3,
)
from core.vastValidator import VastValidator
from core.dto.event import Event
from core.constants import UNKNOWN
from core.dto.event import EventType


@description(
    "This will test a simple scenario, that we are sending `partnerDemandFeePercentage` in the alignment"
)
@pytest.mark.regression
def test_opportunity_event_demand_fee():
    case = Case("test_opportunity_event_demand_fee")
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.VIDEOTRUEFIRSTCALL
    event.beacon_event_type = EventType.VIDEOTRUEFIRSTCALL.name
    # Checking the parameter in the kafka message
    event.partner_demand_fee_percentage = "20.0"

    vast_result.assert_vast_xml().assert_ad_count(1)

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)
