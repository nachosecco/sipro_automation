import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description(
    "Will check that a bidder with custom extensions are in the request send to to the bidder"
)
@pytest.mark.regression
def test_bid_request_custom_ext():
    case = Case("test_bid_request_custom_ext")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    auction_validator = vast_result.validate_rtb_auction()

    bidders = auction_validator.bidders
    bid_request = bidders[0].bid_requests

    ext_request_level = bid_request[0].get("ext", None)
    if ext_request_level is None:
        logging.error(
            "we are expecting that there is a ext object in the top level bid request"
        )
        assert False

    # asserting a simple value extension

    ext_test_1 = ext_request_level.get("custom_extension_test1", None)
    if ext_test_1 is None:
        logging.error(
            "we are expecting that the key custom_extension_test1 not to in the bid request"
        )
        assert False

    if ext_test_1 != "custom_extension_value":
        logging.error(
            "we are expecting that the key custom_extension_value has the value custom_extension_test1"
        )
        assert False
