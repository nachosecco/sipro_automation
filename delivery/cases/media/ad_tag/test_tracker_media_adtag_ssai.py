import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description("A regression test to validate ssai param in ad tags in tracker and media")
@pytest.mark.regression
def test_tracker_media_adtag_ssai():
    case = Case("test_tracker_media_adtag_ssai")
    vpc = case.vpc
    vpc.ssai = "3"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    assert_media_tags = vast_result.assert_vast_xml().assertMediaTags()
    assert_media_tags.ad_tag("ssai", vpc.ssai)

    assert_tracker_tags = vast_result.assertXML().assertTrackerTags(
        "bidder-guid.delivery.automation"
    )
    assert_tracker_tags.ad_tag("ssai", vpc.ssai)
