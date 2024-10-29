import logging

import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator

@pytest.mark.regression
@description(
	"In a placement that does allow multiple imp objects in request "
	"that is align to a private and public deal with same buyer "
	"a pod max duration 120sec, it will have 4 impression objs in the vast"
	"and a responses that:"
	" in imp 1 has the private deal"
	" in imp 2 has the public deal"
	" in imp 3 has the open auction"
	" im imp 4 has the open auction"
	" then there should be 4 winners"
)
def test_multiple_imp_objects_adpod_duration_120sec_on_private_public_deals():
	case = Case("test_multiple_imp_objects_adpod_duration_120sec_on_private_public_deals")
	vpc = case.vpc

	vpc.pod_max_dur = "120"

	# This would execute the framework
	vast_result = VastValidator().test(vpc)

	# Validate the VAST Response
	vast_result.assert_case(case)

	vast_result.assert_vast_xml().assert_ad_count(4)

	bid_request = vast_result.validate_rtb_bid_request().bid_request

	impressions = bid_request["imp"]

	if len(impressions) != 4:
		logging.error("we are expecting 4 impressions, in the request")
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

	if "CP-4730_private" != imp1_pmp_deals[0].get("id"):
		logging.error(
			"we are expecting the deal CP-4730_private in the impression id 1"
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

	if "CP-4730_public" != imp2_pmp_deals[0].get("id"):
		logging.error("we are expecting the deal CP-4730_public in the impression id 2")
		assert False

	# assertion for impression id 3
	imp3_pmp = impressions[2].get("pmp", None)

	if imp3_pmp is not None:
		logging.error("we are expecting 0 pmp object in impression 3 object")
		assert False

	# assertion for impression id 4
	imp4_pmp = impressions[3].get("pmp", None)

	if imp4_pmp is not None:
		logging.error("we are expecting 0 pmp object in impression 3 object")
		assert False