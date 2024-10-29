import pytest
from core.Description import description
from core.vastValidator import VastValidator

from core.case import Case


@description(
    "Test when eids is passed, bid request v2.6 should have eids in user and user.ext object"
)
@pytest.mark.regression
def test_user_eid_param():
    case = Case("test_user_eid_param")

    vpc = case.vpc
    vpc.eid = "W3sidWlkcyI6W3siaWQiOiJwdWJjaWQub3JnIiwiYXR5cGUiOiJpbnRlZ2VyIiwiZXh0Ijp7fX0seyJpZCI6InVpZDEyIiwiYXR5cGUiOiJpbnRlZ2VyIiwiZXh0Ijp7fX0seyJpZCI6InVpZDEzIiwiYXR5cGUiOiJpbnRlZ2VyIiwiZXh0Ijp7fX1dLCJzb3VyY2UiOiJzdHJpbmciLCJleHQiOnt9fSx7InVpZHMiOlt7ImlkIjoidWlkMjEiLCJhdHlwZSI6ImludGVnZXIiLCJleHQiOnt9fSx7ImlkIjoidWlkMjIiLCJhdHlwZSI6ImludGVnZXIiLCJleHQiOnt9fSx7ImlkIjoidWlkMjMiLCJhdHlwZSI6ImludGVnZXIiLCJleHQiOnt9fV0sInNvdXJjZSI6InN0cmluZyIsImV4dCI6e319XQ"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected("test_user_eid_param")
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    assert bid_request_validator.is_eid_as_expected("pubcid.org")


@description(
    "Test when invalid eids is passed, bid request v2.6 should be raised without eids"
)
@pytest.mark.regression
def test_user_invalid_eid_param():
    case = Case("test_user_invalid_eid_param")

    vpc = case.vpc
    vpc.eid = (
        "eyJ1aWRzIjpbeyJpZCI6InB1YmNpZC5vcmciLCJhdHlwZSI6ImludGVnZXIiLCJleHQiOnt9fQ=="
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_user_invalid_eid_param"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    assert bid_request_validator.is_eid_empty()
