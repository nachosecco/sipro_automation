import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test a placement that exists and check that is 404.
@pytest.mark.regression
def test_get_404_delivery_server():
    case = Case("test_example_delivery_not_found")  # This is the file to test this case

    vpc = case.vpc
    vpc.uid = "THE_VOID"

    vast_result = VastValidator().test(vpc, 404)  # This would execute the framework
    vast_result.assertLogsDelivery(["Placement THE_VOID not found."])

    vast_result.assertCase(case)  # This will execute the all assertions in the case
