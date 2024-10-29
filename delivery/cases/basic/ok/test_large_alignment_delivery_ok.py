import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "Validate a placement with a large (more than 128K) alignment is found and returns ok"
)
def test_large_alignment_delivery_ok():
    case = Case("test_large_alignment_delivery_ok")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)
    vast_result.assert_vast_xml().assert_ad_count(11)
