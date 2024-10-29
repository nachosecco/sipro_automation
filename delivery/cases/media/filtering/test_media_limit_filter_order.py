import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


@description(
    "A regression test to validate the order for Media Limit Filter with "
    "Domain & MinCPM Filters, using VPC parameters"
)
@pytest.mark.regression
def test_media_limit_filter_order():
    case = Case("test_media_limit_filter_order")
    vpc = case.vpc

    # Media Limit & Domain filters
    assert_media_count(case, vpc, "ford.com", "[REPLACE]", 2)
    assert_media_count(case, vpc, "tesla.com", "[REPLACE]", 3)

    # Media Limit & MinCPM filters
    assert_media_count(case, vpc, "[REPLACE]", "7.0", 2)
    assert_media_count(case, vpc, "[REPLACE]", "5.0", 3)


def assert_media_count(case, vpc, blocked_domain, min_price, count):
    vpc.regenerate_automation_framework()
    vpc.badv = blocked_domain
    vpc.min_price = min_price
    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)
    vast_xml = vast_result.assert_vast_xml()
    vast_xml.assert_ad_count(count)
