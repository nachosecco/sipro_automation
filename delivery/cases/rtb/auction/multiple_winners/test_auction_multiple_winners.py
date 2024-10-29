import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "In a placement that allows 3 winners and vpc is a apod size=3, it will have 3 ads winning in the vast"
)
def test_rtb_multiple_winners_has_3_wins_with_pod_by_size():
    case = Case("test_rtb_multiple_winners_has_3_wins_with_pod_by_size")
    vpc = case.vpc
    vpc.pod_size = "3"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
@description(
    "In a placement that allows 3 winners and vpc is a apod duration=30, it will have 3 ads winning in the vast"
)
def test_rtb_multiple_winners_has_3_wins_with_pod_by_duration():
    case = Case("test_rtb_multiple_winners_has_3_wins_with_pod_by_duration")
    vpc = case.vpc
    vpc.pod_max_dur = "30"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(3)
