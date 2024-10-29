import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@description(
    "The plcmt flag should exists as 1 in bid request if placement is mobile for VAST 2.5"
)
@pytest.mark.regression
def test_bid_request_plcmt_1_rtb2_5():
    case = Case("test_bid_request_plcmt")  # This is the file to test this case

    # This would execute the framework
    vast_result = VastValidator().test(case.vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    bid_request_validator.is_plcmt_expected(1)


@description(
    "The plcmt flag should exists as 1 in bid request if placement is mobile for VAST 2.6"
)
@pytest.mark.regression
def test_bid_request_plcmt_1_rtb2_6():
    case = Case("test_bid_request_plcmt_2_6")  # This is the file to test this case

    # This would execute the framework
    vast_result = VastValidator().test(case.vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    bid_request_validator.is_plcmt_expected(1)
