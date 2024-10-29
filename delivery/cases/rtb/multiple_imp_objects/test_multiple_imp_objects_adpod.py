import pytest
import logging

from core.adPodAssertor import adPod
from core.case import Case
from core.Description import description
from core.vastValidator import VastValidator
from core.dto.bidder import Bidder
from core.dto.event import EventType


@pytest.mark.regression
@description(
    "This is a test with multiple impression objects in an auction with 2 winners"
    "Bidder A -> impression id 1 has a bid of 20 and impression id 2 has a bid of 30"
    "Bidder B -> impression id 1 has a bid of 40 and impression id 2 has a bid of 20"
    "Bidder B should win impression 1 with a price of 40 "
    "Bidder A should win impression 2 with a price of 30"
)
def test_multiple_imp_objects_adpod_size_2():
    case = Case("test_multiple_imp_objects_adpod_size_2")

    vpc = case.vpc

    vpc.pod_size = "2"

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)

    # we are expecting to have 2 winners in the auction
    vast_result.assert_vast_xml().assert_ad_count(2)

    expected_adpod = adPod()
    expected_adpod.pod_size = 2

    # we are expecting that the winners to have the pod sequences
    vast_result.assert_adpod().does_vast_have_the_expected_pod(expected_adpod)


@pytest.mark.regression
@description(
    "This is a test with multiple impression objects in an auction with 3 winners"
    "Impression id 1 has a bid of 40"
    "Impression id 2 has a bid of 20"
    "Impression id 3 has a bid of 25"
)
def test_multiple_imp_objects_adpod_size_3():
    case = Case("test_multiple_imp_objects_adpod_size_3")

    vpc = case.vpc

    vpc.pod_size = "3"

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)

    # we are expecting to have 3 winners in the auction
    vast_result.assert_vast_xml().assert_ad_count(3)

    expected_adpod = adPod()
    expected_adpod.pod_size = 3

    # we are expecting that the winners to have the pod sequences
    vast_result.assert_adpod().does_vast_have_the_expected_pod(expected_adpod)


@pytest.mark.regression
@description(
    "This is a test with multiple impression objects in an auction with 4 winners"
    "Bidder A -> impId 1 bid of 20 and impId 2 bid of 30"
    "Bidder B -> impId 1 bid of 40 and impId 2 bid of 20"
    "Bidder C -> impId 1 bid of 10 and impId 2 bid of 15 and impId 3 bid of 30 and ImpId 4 bid of 100"
    "Bidder D -> impId 1 bid of 10 and impId 2 bid of 20 and impId 3 bid of 90 and ImpId 4 bid of 20"
    "Bidder B should win impression 1 with a price of 40 "
    "Bidder A should win impression 2 with a price of 30"
    "Bidder D should win impression 3 with a price of 90"
    "Bidder C should win impression 4 with a price of 100"
)
def test_multiple_imp_objects_adpod_duration_120():
    case = Case("test_multiple_imp_objects_adpod_duration_120")

    vpc = case.vpc

    vpc.pod_max_dur = "120"

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)

    # we are expecting to have 4 winners in the auction
    vast_result.assert_vast_xml().assert_ad_count(4)

    expected_adpod = adPod()
    expected_adpod.ads_duration = 120

    # we are expecting that the winners to have the pod sequences
    vast_result.assert_adpod().does_vast_have_the_expected_pod(expected_adpod)


@pytest.mark.regression
@description(
    "This is a test with multiple impression objects in an auction with 10 winners but the pod size sent 20"
    "we have cap of imp object 10 "
)
def test_multiple_max_imp_objects_size_10():
    case = Case("test_multiple_max_imp_objects_size_10")

    vpc = case.vpc

    vpc.pod_size = "20"

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)

    # we are expecting to have 3 winners in the auction
    vast_result.assert_vast_xml().assert_ad_count(10)

    expected_adpod = adPod()
    expected_adpod.pod_size = 10

    # we are expecting that the winners to have the pod sequences
    vast_result.assert_adpod().does_vast_have_the_expected_pod(expected_adpod)


@pytest.mark.regression
@description(
    "This is a test with multiple impression objects in an auction with 4 winners when only define duration"
    "we have cap of imp object 4 when duration is defne only "
)
def test_multiple_max_imp_objects_cap_size_4():
    case = Case("test_multiple_max_imp_objects_cap_size_4")

    vpc = case.vpc

    vpc.pod_max_dur = "120"

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)

    # we are expecting to have 3 winners in the auction
    vast_result.assert_vast_xml().assert_ad_count(4)

    expected_adpod = adPod()
    expected_adpod.pod_size = 4

    # we are expecting that the winners to have the pod sequences
    vast_result.assert_adpod().does_vast_have_the_expected_pod(expected_adpod)


def test_multiple_imp_invalid_bid_response():
    case = Case("test_multiple_imp_invalid_bid_response")

    vpc = case.vpc

    vpc.pod_size = "2"

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assert_case(case)

    # we are expecting to have 3 winners in the auction
    vast_result.assert_vast_xml().assert_ad_count(0)

    auction_validator = vast_result.validate_rtb_auction()
    bidders = auction_validator.bidders
    if not len(bidders) == 1:
        logging.error("We are only expecting only 1 bidder in the request")
        assert False

    if not len(bidders[0].bid_responses) == 1:
        logging.error("We are expecting only 1 bidder response")
        assert False

    if not len(bidders[0].bid_responses[0].seat_bids) == 1:
        logging.error("We are expecting 2 bids in the response")
        assert False

    event = case.event
    event.event_type = EventType.oldRtbAuctionEvent
    lost_bidder = Bidder()
    lost_bidder.bid_loss_reason_code = "INVALID_IMPRESSION_ID_IN_BID"
    event.loss_reason_code = "INVALID_IMPRESSION_ID_IN_BID"
    vast_result.assert_event().assert_expected_event_in_the_log(event)
