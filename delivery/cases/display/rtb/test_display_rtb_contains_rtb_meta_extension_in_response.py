import logging

import pytest

from core.Description import description
from core.case import Case
from core.validator.DisplayPlacementValidator import DisplayPlacementValidator


@pytest.mark.regression
@description("""Assert the response contains a rtb-meta in the response""")
def test_display_rtb_contains_meta_extension_in_response():
    case = Case("test_display_rtb_contains_meta_extension_in_response")

    vpc = case.vpc
    dpl_result = DisplayPlacementValidator().test(vpc)

    dlp_content = dpl_result.dlp_response_content

    media = dlp_content.get("media", None)

    if media is None or len(media) == 0:
        logging.error("There is no media in the display controller media response")
        assert False
    first_media = media[0]

    code = first_media.get("code", None)

    exists_rtb_extension = "rtb-meta" in code

    if not exists_rtb_extension:
        logging.error(
            "We are expecting that rtb-meta extension will be part of the response of a media"
        )
        assert False
