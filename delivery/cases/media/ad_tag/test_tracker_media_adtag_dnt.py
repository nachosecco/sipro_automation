import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description("A regression test to validate dnt param in ad tags in tracker and media")
@pytest.mark.regression
def test_tracker_media_adtag_dnt():
    case = Case("test_tracker_media_adtag_dnt")
    vpc = case.vpc
    vpc.dnt = "1"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    assert_media_tags = vast_result.assert_vast_xml().assertMediaTags()
    assert_media_tags.ad_tag("dnt", vpc.dnt)
