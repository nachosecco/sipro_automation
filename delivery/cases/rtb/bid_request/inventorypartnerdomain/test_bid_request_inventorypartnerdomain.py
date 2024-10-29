import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@description(
    "Test when inventory partner domain is turn on for bid request v2.6 have inventorypartnerdomain in app object"
)
@pytest.mark.regression
def test_bid_request_inventory_partner_domain_rtb26():
    case = Case("test_bid_request_inventory_partner_domain_rtb26")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()

    assert bid_request_validator.is_inventory_partner_domain_as_expected_rtb26(
        "CP-4438.com"
    )


@description(
    "Test when inventory partner domain is turn on for bid request v2.5 have inventorypartnerdomain in app.ext object"
)
@pytest.mark.regression
def test_bid_request_inventory_partner_domain_rtb25():
    case = Case("test_bid_request_inventory_partner_domain_rtb25")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()

    assert bid_request_validator.is_inventory_partner_domain_as_expected_rtb25(
        "CP-4438.com"
    )
