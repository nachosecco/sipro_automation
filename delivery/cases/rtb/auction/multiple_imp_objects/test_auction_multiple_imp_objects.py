import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
	"In a placement that does not allow multiple imp objects in request then there should be only 1 auction winner"
	" from multiples responses"
)
def test_multiple_responses_of_imp_with_only_1_request():
	case = Case("test_multiple_responses_of_imp_with_only_1_request")
	vpc = case.vpc

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	auction_validator = vast_result.validate_rtb_auction()
	bidders = auction_validator.bidders
	if not len(bidders) == 1:
		logging.error("We are only expecting only 1 bidder in the request")
		assert False

	if not len(bidders[0].bid_responses) == 1:
		logging.error("We are expecting only 1 bidder response")
		assert False

	if not len(bidders[0].bid_responses[0].seat_bids) == 3:
		logging.error("We are expecting 3 bids in the response")
		assert False

	vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to a private and public deal with same buyer "
	"and a responses that:"
	" in imp 1 has the private deal"
	" in imp 2 has the public deal"
	" in imp 3 has the open auction"
	" then there should be 3 winners"
)
def test_multiple_imp_with_private_and_public_deals():
	case = Case("test_multiple_imp_with_private_and_public_deals")
	vpc = case.vpc

	vpc.pod_size = "3"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(3)

	bid_request = vast_result.validate_rtb_bid_request().bid_request

	impressions = bid_request["imp"]

	if len(impressions) != 3:
		logging.error("we are expecting 3 impressions, in the request")
		assert False

	# assertion for impression id 1
	imp1_pmp = impressions[0].get("pmp", None)

	if imp1_pmp is None:
		logging.error("we are expecting 1 pmp object in impression 1 object")
		assert False

	imp1_pmp_auction_type = imp1_pmp.get("private_auction", None)

	if imp1_pmp_auction_type is None or imp1_pmp_auction_type != 1:
		logging.error(
			"we are expecting in the impression id 1 in pmp object that auction type should be 1"
		)
		assert False

	imp1_pmp_deals = imp1_pmp.get("deals", [])

	if len(imp1_pmp_deals) != 1:
		logging.error("we are expecting only 1 deal in the impression id 1")
		assert False

	if "CP-3584_private" != imp1_pmp_deals[0].get("id"):
		logging.error(
			"we are expecting the deal CP-3584_private in the impression id 1"
		)
		assert False

	# assertion for impression id 2
	imp2_pmp = impressions[1].get("pmp", None)

	if imp2_pmp is None:
		logging.error("we are expecting 1 pmp object in impression 2 object")
		assert False

	imp2_pmp_auction_type = imp2_pmp.get("private_auction", None)

	if imp2_pmp_auction_type is None or imp2_pmp_auction_type != 0:
		logging.error(
			"we are expecting in the impression id 2 in pmp object that auction type should be 0"
		)
		assert False

	imp2_pmp_deals = imp2_pmp.get("deals", [])

	if len(imp2_pmp_deals) != 1:
		logging.error("we are expecting only 1 deal in the impression id 2")
		assert False

	if "CP-3584_public" != imp2_pmp_deals[0].get("id"):
		logging.error("we are expecting the deal CP-3584_public in the impression id 2")
		assert False

	# assertion for impression id 3
	imp3_pmp = impressions[2].get("pmp", None)

	if imp3_pmp is not None:
		logging.error("we are expecting 0 pmp object in impression 3 object")
		assert False


@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to 2 public deal with same buyer "
	"and a responses that:"
	" in imp 1 has the public deals"
	" in imp 2 has open auction"
	" then there should be 2 winners"
)
def test_multiple_imp_with_only_public_deals():
	case = Case("test_multiple_imp_with_only_public_deals")
	vpc = case.vpc

	vpc.pod_size = "2"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(2)

	bid_request = vast_result.validate_rtb_bid_request().bid_request

	impressions = bid_request["imp"]

	if len(impressions) != 2:
		logging.error("we are expecting 2 impressions, in the request")
		assert False

	# assertion for impression id 1
	imp1_pmp = impressions[0].get("pmp", None)

	if imp1_pmp is None:
		logging.error("we are expecting 1 pmp object in impression 1 object")
		assert False

	imp1_pmp_auction_type = imp1_pmp.get("private_auction", None)

	if imp1_pmp_auction_type is None or imp1_pmp_auction_type != 0:
		logging.error(
			"we are expecting in the impression id 1 in pmp object that auction type should be 1"
		)
		assert False

	imp1_pmp_deals = imp1_pmp.get("deals", [])

	if len(imp1_pmp_deals) != 2:
		logging.error("we are expecting only 2 deals in the impression id 1")
		assert False

	# assertion for impression id 2
	imp2_pmp = impressions[1].get("pmp", None)

	if imp2_pmp is not None:
		logging.error("we are expecting 0 pmp object in impression id 2")
		assert False


@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to 2 private deal with same buyer "
	"and a responses that:"
	" in imp 1 has the private deals"
	" in imp 2 has open auction"
	" then there should be 1 winners"
)
def test_multiple_imp_with_only_private_deals():
	case = Case("test_multiple_imp_with_only_private_deals")
	vpc = case.vpc

	vpc.pod_size = "2"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(1)

	bid_request = vast_result.validate_rtb_bid_request().bid_request

	impressions = bid_request["imp"]

	if len(impressions) != 1:
		logging.error("we are expecting 1 impressions, in the request")
		assert False

	# assertion for impression id 1
	imp1_pmp = impressions[0].get("pmp", None)

	if imp1_pmp is None:
		logging.error("we are expecting 1 pmp object in impression 1 object")
		assert False

	imp1_pmp_auction_type = imp1_pmp.get("private_auction", None)

	if imp1_pmp_auction_type is None or imp1_pmp_auction_type != 1:
		logging.error(
			"we are expecting in the impression id 1 in pmp object that auction type should be 1"
		)
		assert False

	imp1_pmp_deals = imp1_pmp.get("deals", [])

	if len(imp1_pmp_deals) != 2:
		logging.error("we are expecting only 2 deals in the impression id 1")
		assert False


@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to a private and public deal with same buyer "
	"and a responses that:"
	" in imp 1 has the private deal"
	" in imp 2 has the public deal"
	" in imp 3 has the open auction"
	" then there should be 3 winners"
)
def test_multiple_imp_with_private_and_public_deals():
	case = Case("test_multiple_imp_with_private_and_public_deals")
	vpc = case.vpc

	vpc.pod_size = "3"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(3)

	bid_request = vast_result.validate_rtb_bid_request().bid_request

	impressions = bid_request["imp"]

	if len(impressions) != 3:
		logging.error("we are expecting 3 impressions, in the request")
		assert False

	# assertion for impression id 1
	imp1_pmp = impressions[0].get("pmp", None)

	if imp1_pmp is None:
		logging.error("we are expecting 1 pmp object in impression 1 object")
		assert False

	imp1_pmp_auction_type = imp1_pmp.get("private_auction", None)

	if imp1_pmp_auction_type is None or imp1_pmp_auction_type != 1:
		logging.error(
			"we are expecting in the impression id 1 in pmp object that auction type should be 1"
		)
		assert False

	imp1_pmp_deals = imp1_pmp.get("deals", [])

	if len(imp1_pmp_deals) != 1:
		logging.error("we are expecting only 1 deal in the impression id 1")
		assert False

	if "CP-3584_private" != imp1_pmp_deals[0].get("id"):
		logging.error(
			"we are expecting the deal CP-3584_private in the impression id 1"
		)
		assert False

	# assertion for impression id 2
	imp2_pmp = impressions[1].get("pmp", None)

	if imp2_pmp is None:
		logging.error("we are expecting 1 pmp object in impression 2 object")
		assert False

	imp2_pmp_auction_type = imp2_pmp.get("private_auction", None)

	if imp2_pmp_auction_type is None or imp2_pmp_auction_type != 0:
		logging.error(
			"we are expecting in the impression id 2 in pmp object that auction type should be 0"
		)
		assert False

	imp2_pmp_deals = imp2_pmp.get("deals", [])

	if len(imp2_pmp_deals) != 1:
		logging.error("we are expecting only 1 deal in the impression id 2")
		assert False

	if "CP-3584_public" != imp2_pmp_deals[0].get("id"):
		logging.error("we are expecting the deal CP-3584_public in the impression id 2")
		assert False

	# assertion for impression id 3
	imp3_pmp = impressions[2].get("pmp", None)

	if imp3_pmp is not None:
		logging.error("we are expecting 0 pmp object in impression 3 object")
		assert False


@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to 2 public deal with same buyer "
	"and a responses that:"
	" in imp 1 has the public deals"
	" in imp 2 has open auction"
	" then there should be 2 winners"
)
def test_multiple_imp_with_only_public_deals():
	case = Case("test_multiple_imp_with_only_public_deals")
	vpc = case.vpc

	vpc.pod_size = "2"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(2)

	bid_request = vast_result.validate_rtb_bid_request().bid_request

	impressions = bid_request["imp"]

	if len(impressions) != 2:
		logging.error("we are expecting 2 impressions, in the request")
		assert False

	# assertion for impression id 1
	imp1_pmp = impressions[0].get("pmp", None)

	if imp1_pmp is None:
		logging.error("we are expecting 1 pmp object in impression 1 object")
		assert False

	imp1_pmp_auction_type = imp1_pmp.get("private_auction", None)

	if imp1_pmp_auction_type is None or imp1_pmp_auction_type != 0:
		logging.error(
			"we are expecting in the impression id 1 in pmp object that auction type should be 1"
		)
		assert False

	imp1_pmp_deals = imp1_pmp.get("deals", [])

	if len(imp1_pmp_deals) != 2:
		logging.error("we are expecting only 2 deals in the impression id 1")
		assert False

	# assertion for impression id 2
	imp2_pmp = impressions[1].get("pmp", None)

	if imp2_pmp is not None:
		logging.error("we are expecting 0 pmp object in impression id 2")
		assert False


@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to 1 private deal and public deal with same buyer "
	"and a responses that:"
	" in imp 1 has the private deals"
	" in imp 2 has open auction with invalid deal"
	" in imp 3 has open auction with invalid deal"
	" then there should be 3 winners"
)
def test_multiple_imp_with_private_public_and_invalid_deals():
	case = Case("test_multiple_imp_with_private_public_and_invalid_deals")
	vpc = case.vpc

	vpc.pod_size = "3"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(3)


@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to 1 private deal "
	"and placement tag has pod size 4"
	"and a responses that:"
	" there should be only one multiple impression in the bid request"
	" in imp 1 has the private deal"
)
def test_multiple_imp_with_only_one_private_deal():
	case = Case("test_multiple_imp_with_only_one_private_deal")
	vpc = case.vpc

	vpc.pod_size = "4"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(1)

	bid_request = vast_result.validate_rtb_bid_request().bid_request

	impressions = bid_request["imp"]

	assert (
			len(impressions) == 1
	), f"we are expecting 1 impression in the bid request, in the request found impression = {len(impressions)}"

	# assertion for impression id 1
	imp1_pmp = impressions[0].get("pmp", None)

	assert (
			imp1_pmp is not None
	), f"we are expecting 1 pmp object in impression 1 object"

	imp1_pmp_auction_type = imp1_pmp.get("private_auction", None)

	assert (
			imp1_pmp_auction_type is not None and imp1_pmp_auction_type == 1
	), f"we are expecting in the impression id 1 in pmp object that auction type should be 1"

	imp1_pmp_deals = imp1_pmp.get("deals", [])

	assert (
			len(imp1_pmp_deals) == 1
	), f"we are expecting only 1 deal in the impression id 1"


@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to 1 private deal and public deal with same buyer "
	"and multiple impression is turned off at placement"
	"and a responses that:"
	" only 1 imp object"
	" 2 deals objects in imp1 "

)
def test_multiple_imp_with_private_and_public_deals_turnoff_for_placement():
	case = Case("test_multiple_imp_with_private_and_public_deals_turnoff_for_placement")
	vpc = case.vpc

	vpc.pod_size = "3"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(1)

	bid_request = vast_result.validate_rtb_bid_request().bid_request

	impressions = bid_request["imp"]

	assert (
			len(impressions) == 1
	), f"we are expecting 1 impression in the bid request, in the request found impression = {len(impressions)}"

	# assertion for impression id 1
	imp1_pmp = impressions[0].get("pmp", None)

	assert (
			imp1_pmp is not None
	), f"we are expecting 1 pmp object in impression 1 object"

	imp1_pmp_auction_type = imp1_pmp.get("private_auction", None)

	assert (
			imp1_pmp_auction_type is not None and imp1_pmp_auction_type == 1
	), f"we are expecting in the impression id 1 in pmp object that auction type should be 1"

	imp1_pmp_deals = imp1_pmp.get("deals", [])

	assert (
			len(imp1_pmp_deals) == 2
	), f"we are expecting 2 deals in the impression id 1"
