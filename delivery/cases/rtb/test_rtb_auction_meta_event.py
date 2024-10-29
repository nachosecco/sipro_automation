import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator
from core.vastXMLAssertor import get_impressions

RTB_META_PARAMETER = "&rm="


@pytest.mark.regression
@description(
    "This is a case to check if we have rtb-meta for impression and track events"
)
def test_rtb_meta_in_impression_event():
    case = Case("test_rtb_meta_in_impression_event")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    ads = vast_result.assert_vast_xml().root_element_xml.findall("Ad")
    for ad in ads:
        impressions = get_impressions(ad)

        for impression in impressions:

            if "ev=rollimp" in impression.text:

                # Checking we have the rtb for impression event
                if RTB_META_PARAMETER not in impression.text:
                    logging.error(
                        "The rtb meta was not found in the event of impression `ev=rollimp` was not found"
                    )
                    assert False

    tag_tracking = vast_result.assert_vast_xml().root_element_xml.findall(
        "./Ad/InLine/Creatives/Creative/Linear/TrackingEvents/Tracking"
    )

    for tracking in tag_tracking:
        event = tracking.get("event")

        if RTB_META_PARAMETER not in tracking.text:
            logging.error(
                f"The event {event} does not contains the rtb-meta please check the vast response."
            )
            assert False
