import pytest
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator


@description(
    "DNT flag should exists as true in bid request if dnt = 1 passed in vpc request"
)
@pytest.mark.regression
def test_bid_request_do_not_track_out_true():
    case = Case(
        "test_bid_request_do_not_track_out_true"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.dnt = "1"
    vpc.page_url = "page_url"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    bid_request_validator.is_device_dnt_as_expected(1)


@description(
    "DNT flag should exists as false in bid request if dnt = 0 passed in vpc request"
)
@pytest.mark.regression
def test_bid_request_do_not_track_out_false():
    case = Case(
        "test_bid_request_do_not_track_out_false"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.dnt = "0"
    vpc.page_url = "page_url"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    bid_request_validator.is_device_dnt_as_expected(0)
