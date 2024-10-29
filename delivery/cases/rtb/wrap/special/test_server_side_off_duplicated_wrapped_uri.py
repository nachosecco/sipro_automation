import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "This is test that check when we have duplicated wrapped uri in the VAST response "
    "and server side off it will throw one off"
)
def test_server_side_off_duplicated_wrapped_uri():
    case = Case("test_server_side_off_duplicated_wrapped_uri")

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    vast_result.assert_logs_delivery("Found multiple wrappers with the same VAST URI")

    vast_result.assert_vast_xml().assert_ad_count(1)
