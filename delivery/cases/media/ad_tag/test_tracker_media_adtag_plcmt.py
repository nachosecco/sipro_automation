import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description("A regression test to validate plcmt param in ad tags in tracker and media")
@pytest.mark.regression
def test_tracker_media_adtag_plcmt():

	# validating with correct value, macro value should be set as it is.
	case = Case("test_tracker_media_adtag_plcmt")
	vpc = case.vpc
	vpc.plcmt = "1"
	vast_result = VastValidator().test(vpc)

	vast_result.assert_case(case)

	assert_media_tags = vast_result.assert_vast_xml().assertMediaTags()
	assert_media_tags.ad_tag("plcmt", "1")

	assert_tracker_tags = vast_result.assert_vast_xml().assertTrackerTags(
		"bidder-guid.delivery.automation"
	)
	assert_tracker_tags.ad_tag("plcmt", "1")

	# validating with incorrect input, macro value should set based on placement type.
	vpc.plcmt = "5"
	vast_result = VastValidator().test(vpc)
	vast_result.assert_case(case)

	assert_media_tags = vast_result.assert_vast_xml().assertMediaTags()
	assert_media_tags.ad_tag("plcmt", "1")
