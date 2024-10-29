import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator

DURATION_TAG_10_SECONDS = "https://cdndev.altitude-arena.com/c6internaltestpage/regressiontestpage/vast_duration_10.xml"

DURATION_TAG_15_SECONDS = "https://cdndev.altitude-arena.com/c6internaltestpage/regressiontestpage/vast_duration_15.xml"


@pytest.mark.regression
@description(
    "In a placement that contains 2 bidder with a placement that allows cpm per second"
)
def test_rtb_open_auction_cpm_per_second():
    case = Case("test_rtb_open_auction_cpm_per_second")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    xml = vast_result.assert_vast_xml().root_element_xml

    all_uri = xml.findall("./Ad/Wrapper/VASTAdTagURI")
    if len(all_uri) == 0:
        logging.error("We are expecting a tag of a wrapper of 10 seconds")
        assert False

    tag = all_uri[0].text

    valid_tag = DURATION_TAG_10_SECONDS == tag

    if not valid_tag:
        logging.error("We are expecting a tag of a wrapper of 10 seconds")
        assert False


@pytest.mark.regression
@description(
    """In a placement, and floor =10 with bidders:
    Bidder 1,  Bid = 30, Duration = 30 Sec, Deal = CP_3757_T1
    Bidder 2,  Bid = 20, Duration = 30 Sec, Deal = CP_3757_T1
    Bidder 3,  Bid = 20, Duration = 15 Sec, Open Auction
    Bidder 4,  Bid = 12, Duration = 15 Sec, Open Auction
     It should win bidder 3 win price = 20"""
)
def test_rtb_deal_second_price_and_open_auction_cpm_per_second_scenario_1():

    case = Case("test_rtb_deal_second_price_and_open_auction_cpm_per_second_scenario_1")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    xml = vast_result.assert_vast_xml().root_element_xml

    all_uri = xml.findall("./Ad/Wrapper/VASTAdTagURI")
    if len(all_uri) == 0:
        logging.error(
            "There is no uri, and we are expecting a tag of a wrapper of 15 seconds"
        )
        assert False

    tag = all_uri[0].text

    valid_tag = DURATION_TAG_15_SECONDS == tag

    if not valid_tag:
        logging.error("We are expecting a tag of a wrapper of 15 seconds")
        assert False

    auction_validator = vast_result.validate_rtb_auction()
    auction_validator.is_win_price_as_expected(20)


@pytest.mark.regression
@description(
    """In a placement, and floor =10 with bidders:
    Bidder 1,  Bid = 30, Duration = 15 Sec, Deal = CP_3757_t2
    Bidder 2,  Bid = 25, Duration = 10 Sec, Deal = CP_3757_t2
    Bidder 3,  Bid = 20, Duration = 15 Sec, Open Auction
    Bidder 4,  Bid = 12, Duration = 15 Sec, Open Auction
     It should win bidder 1 win price = 25.1"""
)
def test_rtb_deal_second_price_and_open_auction_cpm_per_second_scenario_2():

    case = Case("test_rtb_deal_second_price_and_open_auction_cpm_per_second_scenario_2")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    xml = vast_result.assert_vast_xml().root_element_xml

    all_uri = xml.findall("./Ad/Wrapper/VASTAdTagURI")
    if len(all_uri) == 0:
        logging.error(
            "There is no uri, and we are expecting a tag of a wrapper of 15 seconds"
        )
        assert False

    tag = all_uri[0].text

    valid_tag = DURATION_TAG_15_SECONDS == tag

    if not valid_tag:
        logging.error("We are expecting a tag of a wrapper of 15 seconds")
        assert False

    auction_validator = vast_result.validate_rtb_auction()
    auction_validator.is_win_price_as_expected(25.1)


@pytest.mark.regression
@description(
    """In a placement, and floor =10 with bidders:
    Bidder 1,  Bid = 30, Duration = 15 Sec, Deal = CP_3757_t3
    Bidder 2,  Bid = 25, Duration = 15 Sec, Deal = CP_3757_t3
    Bidder 3,  Bid = 20, Duration = 15 Sec, Open Auction
    Bidder 4,  Bid = 12, Duration = 15 Sec, Open Auction
     It should win bidder 1 win price = 25.1"""
)
def test_rtb_deal_second_price_and_open_auction_cpm_per_second_scenario_3():

    case = Case("test_rtb_deal_second_price_and_open_auction_cpm_per_second_scenario_3")
    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    xml = vast_result.assert_vast_xml().root_element_xml

    all_uri = xml.findall("./Ad/Wrapper/VASTAdTagURI")
    if len(all_uri) == 0:
        logging.error(
            "There is no uri, and we are expecting a tag of a wrapper of 15 seconds"
        )
        assert False

    tag = all_uri[0].text

    valid_tag = DURATION_TAG_15_SECONDS == tag

    if not valid_tag:
        logging.error("We are expecting a tag of a wrapper of 15 seconds")
        assert False

    auction_validator = vast_result.validate_rtb_auction()
    auction_validator.is_win_price_as_expected(25.1)
