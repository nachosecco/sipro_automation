import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description(
    "Will check that a bidder with response that is not 200 it will have a kafka message"
)
@pytest.mark.regression
def test_bid_response_with_status_not_200_have_kafka_message():
    case = Case("test_bid_response_with_status_not_200_have_kafka_message")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assert_case(case)

    # checking that we have no vast ad
    vast_result.assert_vast_xml().assert_ad_count(0)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    if len(bidders) != 1:
        logging.error("We are expecting 1 bidder for this case")
        assert False

    # checking if the kafka message for rtb is present
    vast_result.assert_logs_delivery(["rtbEvent"])
