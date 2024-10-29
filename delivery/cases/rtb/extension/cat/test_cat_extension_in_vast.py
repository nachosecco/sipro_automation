import pytest

from core.Description import description
from core.assertor.extensionAssertor import ExpectedCategory
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    "test category extension is present in the VAST response and the values are as expected"
)
def test_category_extension_is_ok():
    case = Case("test_category_extension_is_ok")

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # this test cases has 1 ad
    vast_result.assert_vast_xml().assert_ad_count(1)

    expected_categories = [ExpectedCategory(category=["IAB-1"])]

    vast_result.assert_extension().assert_categories_are(expected_categories)
