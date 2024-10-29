import pytest

from core.case import Case
from core.vastValidator import VastValidator
from core.constants import REPLACE


@pytest.mark.regression
def test_bid_request_network_channel_with_values_rtb26():
    """
    Configuration - Regular Placement has one programmatic demand aligned with a bidder version 2.6
    Expected result -
    network and channel name passed in the vast request, should be sent further in the bid request as bidder's
    version is 2.6
    """

    case = Case("test_bid_request_network_channel_with_values_rtb26")

    vpc = case.vpc
    vpc.channel_name = "BBC"
    vpc.network_name = "ABC"
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bid_request_validator.is_rtb_version_as_expected(2.6)
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"
            assert (
                bid_request["app"]["content"].get("network").get("name")
                == vpc.network_name
            ), "Network name didn't match"
            assert (
                bid_request["app"]["content"].get("channel").get("name")
                == vpc.channel_name
            ), "Channel name didn't match"


@pytest.mark.regression
def test_bid_request_network_channel_without_values_rtb26():
    """
    Configuration - Regular Placement has one programmatic demand aligned with a bidder version 2.6
    Expected result -
    network and channel name is not passed in the vast request, bid request should not create the network and
    channel object in bid request
    """
    case = Case("test_bid_request_network_channel_without_values_rtb26")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bid_request_validator.is_rtb_version_as_expected(2.6)
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"

            assert (
                bid_request["app"]["content"].get("network").get("name") == REPLACE
            ), "Network details found when not expected"
            assert (
                bid_request["app"]["content"].get("channel").get("name") == REPLACE
            ), "Channel details found when not expected"


@pytest.mark.regression
def test_bid_request_network_channel_with_values_not_sent_rtb25():
    """
    Configuration - Regular Placement has one programmatic demand aligned with a bidder version 2.5
    Expected result -
    network and channel name is passed in the vast request, bid request should not create the network and
    channel object in bid request as bidder version is not 2.6
    """
    case = Case("test_bid_request_network_channel_with_values_not_sent_rtb25")

    vpc = case.vpc
    vpc.channel_name = "BBC"
    vpc.network_name = "ABC"
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    bid_request_validator = vast_result.validate_rtb_bid_request()
    bidders = bid_request_validator.bidders
    for bidder in bidders:
        bid_request_validator.is_rtb_version_as_expected(2.5)
        for bid_request in bidder.bid_requests:
            assert bid_request, f"Bid_request is not found"

            assert (
                bid_request["app"]["content"].get("network") is None
            ), "Network details found when not expected"
            assert (
                bid_request["app"]["content"].get("channel") is None
            ), "Channel details found when not expected"
