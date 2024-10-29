import pytest
from core.Description import description
from core.case import Case
from core.enums.filterReason import FilterReason
from core.vastValidator import VastValidator


@description(
    "Test to verify that the ad response size is not exceeded when the company configuration is set to 3"
)
@pytest.mark.regression
def test_placement_max_ad_response_size_company_configuration():
    case = Case("test_placement_max_ad_response_size_company_configuration")
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_ad_count(3)
    vast_result.assert_filter(FilterReason.AD_RESPONSE_SIZE_EXCEEDED)


@description(
    "Test to verify that the ad response size is not exceeded when the placement configuration is set to 2"
)
@pytest.mark.regression
def test_placement_max_ad_response_size_placement_override_company_configuration():
    case = Case(
        "test_placement_max_ad_response_size_placement_override_company_configuration"
    )
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_ad_count(2)
    vast_result.assert_filter(FilterReason.AD_RESPONSE_SIZE_EXCEEDED)
