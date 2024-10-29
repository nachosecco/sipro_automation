import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason


@pytest.mark.regression
@description(
	"""Test that a programmatic demand with custom url param targeting filters only requests that do not match rule

	We've set up a single placement with a single programmatic demand aligned that has custom url targeting:
		* content_title of either "*Pet Detective" or "Ace Ventura*"
		* content_genre of "Comedy"
	"""
)
def test_programmatic_targeting_custom_url_expression():
	case = Case("test_programmatic_targeting_custom_url_expression")
	vpc = case.vpc

	# We make our first request with params that are not a match
	vpc.content_title = "Not A Match"
	vpc.content_genre = "Horror"

	vast_result = VastValidator().test(vpc)

	# The programmatic should be filtered and not included in the vast
	vast_result.assertFilter(FilterReason.TARGETING_PARAMS)
	vast_result.assert_vast_xml().assert_ad_count(0)

	# Set up VPC to make a second request that is a match
	vpc.regenerate_automation_framework()

	# Add params that match the rule
	vpc.content_title = "Ace Ventura: When Nature Calls"
	vpc.content_genre = "Comedy"

	vast_result = VastValidator().test(vpc)

	# If there's one media in the vast we know our only aligned programmatic passed targeting checks.
	vast_result.assert_vast_xml().assert_ad_count(1)

