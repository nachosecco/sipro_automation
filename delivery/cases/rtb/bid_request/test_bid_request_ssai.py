import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@description("Test when ssai as 2, bid request v2.6 have ssai in imp object")
@pytest.mark.regression
def test_bid_request_ssai_rtb26():
    case = Case("test_bid_request_ssai_rtb26")

    vpc = case.vpc
    vpc.ssai = "2"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ssai_rtb26"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    assert bid_request_validator.is_ssai_as_expected_rtb26(2)


@description(
    "Test when ssai as 2, bid request v2.5 have ssai in impression custom data"
)
@pytest.mark.regression
def test_bid_request_ssai_rtb25():
    case = Case("test_bid_request_ssai_rtb25")

    vpc = case.vpc
    vpc.ssai = "2"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ssai_rtb25"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    assert bid_request_validator.is_ssai_as_expected_rtb25(2)
