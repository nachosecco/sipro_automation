import logging

import pytest

from core.Description import description
from core.case import Case
from core.validator.DisplayPlacementValidator import DisplayPlacementValidator


@pytest.mark.regression
@description("""Assert the trackers of placements are in the media""")
def test_display_trackers():
    case = Case("test_display_trackers")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)

    dlp_content = dpl_result.dlp_response_content

    media = dlp_content.get("media", None)

    if media is None or len(media) == 0:
        logging.error("There is no media in the display controller media response")
        assert False
    first_media = media[0]

    trackers = first_media.get("trackers", None)

    if trackers is None:
        logging.error("There is no a key with trackers name")
        assert False

    impression_trackers = trackers.get("ip", None)

    if impression_trackers is None or len(impression_trackers) != 1:
        logging.error(
            "we are expecting to have 1 tracker, and there was none in the response of the controller"
        )
        assert False

    expected_tracker = "https:\\/\\/example.com?my_transation_id="
    found_the_tracker = impression_trackers[0].startswith(expected_tracker)

    if not (found_the_tracker):
        logging.error(
            f"The tracker {expected_tracker} was not found in {impression_trackers[0]} "
        )
        assert False
