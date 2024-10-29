import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description("check there is not duplicated impression tag in vast ad")
def test_tracker_should_no_be_duplicated_tracker_in_impression_tag_in_vast():
    case = Case(
        "test_tracker_should_no_be_duplicated_tracker_in_impression_tag_in_vast"
    )

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # there should only 1 ad in the vast
    vast_result.assert_vast_xml().assert_ad_count(1)

    impression_tags = vast_result.assert_vast_xml().getAllImpressions()
    impression_tags_set = set(impression_tags)

    if len(impression_tags) != len(impression_tags_set):
        logging.error("We should not have duplicated tag of impression")
        assert False
