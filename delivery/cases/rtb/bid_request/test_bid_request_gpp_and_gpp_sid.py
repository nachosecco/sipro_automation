import pytest
from core.case import Case

from core.Description import description
from core.vastValidator import VastValidator


@description("Gpp and Gpp Sid is sent to RTB placement, gets included in bid request")
@pytest.mark.regression
def test_bid_request_gpp_and_gpp_sid_params():
    case = Case("test_bid_request_gpp_and_gpp_sid_params")

    vpc = case.vpc
    vpc.gpp = "DBABRg~BAAAABA"
    vpc.gpp_sid = "9"
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bid_request_validator.is_rtb_version_as_expected(2.6)
        for bid_request in bidder.bid_requests:
            assert bid_request, "Bid_request is not found"
            assert bid_request["regs"]["gpp"] == vpc.gpp, "GPP string didn't match"
            assert bid_request["regs"]["gpp_sid"][0] == int(
                vpc.gpp_sid
            ), "GPP sid didn't match"
            assert (
                bid_request["regs"]["ext"]["gpp"] == vpc.gpp
            ), "GPP string in ext didn't match"
            assert bid_request["regs"]["ext"]["gpp_sid"][0] == int(
                vpc.gpp_sid
            ), "GPP sid in ext didn't match"


@description(
    "Gpp and Gpp Sid is not sent to RTB placement, then not added to bid request"
)
@pytest.mark.regression
def test_bid_request_empty_gpp_and_gpp_sid_params():
    case = Case("test_bid_request_empty_gpp_and_gpp_sid_params")

    vpc = case.vpc
    vpc.gpp = ""
    vpc.gpp_sid = ""
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bid_request_validator.is_rtb_version_as_expected(2.6)
        for bid_request in bidder.bid_requests:
            assert bid_request, "Bid_request is not found"
            assert "gpp" not in bid_request["regs"], "GPP string key was not expected"
            assert "gpp_sid" not in bid_request["regs"], "GPP sid key was not expected"
            assert (
                "gpp" not in bid_request["regs"]["ext"]
            ), "GPP string key was not expected"
            assert (
                "gpp_sid" not in bid_request["regs"]["ext"]
            ), "GPP sid key was not expected"
