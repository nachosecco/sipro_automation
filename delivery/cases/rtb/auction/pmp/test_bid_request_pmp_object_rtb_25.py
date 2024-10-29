import pytest

from core.case import Case
from core.dto.pmp import PMP, Deal
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_bid_request_pmp_object_private_auc_onedemand_rtb25():
    case = Case("test_bid_request_pmp_object_private_auc_onedemand_rtb25")

    vpc = case.vpc
    pmp = PMP()
    pmp.bidder_name = "test_bid_request_pmp_object_private_auc_onedemand_rtb25"
    pmp.private_auction = 1
    deal = Deal()
    deal.id = "seatValDealId1_RTB25"
    deal.bid_floor = 0.01
    deal.bid_floor_cur = "USD"
    deal.wseat = ["seat1"]
    deal.at = 1
    pmp.deals = [deal]

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    vast_result.validate_rtb_auction().are_pmp_objects_valid([pmp])


@pytest.mark.regression
def test_bid_request_pmp_object_private_auc_onedemand_2seats1bidder_rtb25():
    case = Case("test_bid_request_pmp_object_private_auc_onedemand_2seats1bidder_rtb25")

    vpc = case.vpc
    pmp = PMP()
    pmp.bidder_name = (
        "test_bid_request_pmp_object_private_auc_onedemand_2seats1bidder_rtb25"
    )
    pmp.private_auction = 1
    deal = Deal()
    deal.id = "seatValDealId12seats_RTB25"
    deal.bid_floor = 10
    deal.bid_floor_cur = "USD"
    deal.wseat = ["seat1", "seat5"]
    deal.at = 1
    pmp.deals = [deal]

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    vast_result.validate_rtb_auction().are_pmp_objects_valid([pmp])


@pytest.mark.regression
def test_bid_request_pmp_object_public_auc_onedemand_rtb25():
    case = Case("test_bid_request_pmp_object_public_auc_onedemand_rtb25")

    vpc = case.vpc
    pmp = PMP()
    pmp.bidder_name = "test_bid_request_pmp_object_public_auc_onedemand_rtb25"
    pmp.private_auction = 0
    deal = Deal()
    deal.id = "seatValDealId2_RTB25"
    deal.bid_floor = 0.01
    deal.bid_floor_cur = "USD"
    deal.wseat = ["seat2"]
    deal.at = 2
    pmp.deals = [deal]

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    vast_result.validate_rtb_auction().are_pmp_objects_valid([pmp])


@pytest.mark.regression
def test_bid_request_pmp_object_pvt_auc_twodemands_2bidders_rtb25():
    case = Case("test_bid_request_pmp_object_pvt_auc_twodemands_2bidders_rtb25")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    pmp = PMP()
    pmp.bidder_name = (
        "test_bid_request_pmp_object_pvt_auc_twodemands_2bidders_rtb25 [2]"
    )
    pmp.private_auction = 1
    deal = Deal()
    deal.id = "dealPvtAuc_RTB25"
    deal.bid_floor = 0.01
    deal.bid_floor_cur = "USD"
    deal.wseat = ["seat1"]
    deal.at = 1
    pmp.deals = [deal]

    pmp2 = PMP()
    pmp2.bidder_name = (
        "test_bid_request_pmp_object_pvt_auc_twodemands_2bidders_rtb25 [1]"
    )
    pmp2.private_auction = 1
    deal = Deal()
    deal.id = "dealPvtAuc_RTB25"
    deal.bid_floor = 0.01
    deal.bid_floor_cur = "USD"
    deal.wseat = ["seat2"]
    deal.at = 1

    deal2 = Deal()
    deal2.id = "seatValDealId2_RTB25"
    deal2.bid_floor = 0.01
    deal2.bid_floor_cur = "USD"
    deal2.wseat = ["seat2"]
    deal2.at = 2
    pmp2.deals = [deal, deal2]
    vast_result.validate_rtb_auction().are_pmp_objects_valid([pmp, pmp2])


@pytest.mark.regression
def test_bid_request_pmp_object_pub_auc_twodemands_2bidders_rtb25():
    case = Case("test_bid_request_pmp_object_pub_auc_twodemands_2bidders_rtb25")

    vpc = case.vpc
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    pmp = PMP()
    pmp.bidder_name = (
        "test_bid_request_pmp_object_pub_auc_twodemands_2bidders_rtb25 [2]"
    )
    pmp.private_auction = 0
    deal = Deal()
    deal.id = "dealPubAuc_RTB25_2bidders"
    deal.bid_floor = 0.01
    deal.bid_floor_cur = "USD"
    deal.wseat = ["seat2"]
    deal.at = 2
    pmp.deals = [deal]

    pmp2 = PMP()
    pmp2.bidder_name = (
        "test_bid_request_pmp_object_pub_auc_twodemands_2bidders_rtb25 [1]"
    )
    pmp2.private_auction = 0
    deal = Deal()
    deal.id = "dealPubAuc_RTB25_2bidders"
    deal.bid_floor = 0.01
    deal.bid_floor_cur = "USD"
    deal.wseat = ["seat1"]
    deal.at = 2

    deal2 = Deal()
    deal2.id = "dealPubAuc_RTB25_2bidders"
    deal2.bid_floor = 0.01
    deal2.bid_floor_cur = "USD"
    deal2.wseat = ["seat1"]
    deal2.at = 2
    pmp2.deals = [deal, deal2]
    vast_result.validate_rtb_auction().are_pmp_objects_valid([pmp, pmp2])
