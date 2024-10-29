import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
@description(
    """This tests URL query parameter media targeting with spaces in rules for custom parameter value targeting"""
)
def test_media_targeting_param_value_with_spaces_in_targeting_rule():
    case = Case("test_media_targeting_param_value_with_spaces_in_targeting_rule")

    # URL Parameter media targeting rules content_genre=New York Giants content_title=*New York Giants*
    vpc = case.vpc

    # URL Parameter values matches wildcard targeting rules. An Ad will be served.
    vpc.content_genre = "New York Giants"
    vpc.content_title = "New York Giants vs. Dallas Cowboys"
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(1)

    # URL parameter values don't match wildcard targeting rules. No Ad will be served.
    vpc.regenerate_automation_framework()
    vpc.content_genre = "NY Giants"
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(0)

    vpc.regenerate_automation_framework()
    vpc.content_genre = "New York Giants"
    vpc.content_title = "NY Giants vs. Dallas Cowboys"
    vast_result = VastValidator().test(vpc)
    vast_result.assert_vast_xml().assert_ad_count(0)
