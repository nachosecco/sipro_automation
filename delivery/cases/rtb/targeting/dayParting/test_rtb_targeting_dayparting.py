import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "This is case that check day parting for everyday and every hour in rtb targeting is working"
)
def test_rtb_targeting_day_parting_is_ok():
    case = Case("test_rtb_targeting_day_parting_is_ok")

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(1)
