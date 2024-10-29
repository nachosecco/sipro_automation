import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "This is a simple case of how to test that placement in default config and check is ok "
)
def test_example_delivery_ok():
    case = Case("test_example_delivery_ok")  # This is the file to test this case

    vpc = case.vpc

    # This would override the case data
    vpc.content_series = "Moon Knight"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)

    # Extra assertions for this case
    vast_result.assert_logs_delivery("content_series=" + vpc.content_series)
    vast_result.assert_logs_delivery("passed all filters")
