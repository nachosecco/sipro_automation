import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "This test case is to validate that we don't get a concurrent modification exception, "
    "when some have unwrapping on managed media , we should get some ads"
)
def test_unwrap_with_12_managed_will_return_vast_with_ads():

    case = Case("test_unwrap_with_12_managed_will_return_vast_with_ads")

    vpc = case.vpc
    vpc.pod_size = "10"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_not_empty()
