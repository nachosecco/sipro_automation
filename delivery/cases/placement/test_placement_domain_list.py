import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason


@pytest.mark.regression
def test_placement_domain_list_block():
    case = Case("test_placement_domain_list_block")

    vpc = case.vpc
    vpc.page_url = "https://www.blocked-url-example.com"
    vastResult = VastValidator().test(vpc)

    vastResult.assertFilter(FilterReason.PUBLISHER_FILTER)

    vastResult.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_placement_domain_list_block_negative():
    case = Case("test_placement_domain_list_block_negative")

    vpc = case.vpc
    vpc.page_url = "https://www.not-blocked-url-example.com"

    vastResult = VastValidator().test(vpc)

    vastResult.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_placement_domain_list_allow():
    case = Case("test_placement_domain_list_allow")

    vpc = case.vpc
    vpc.page_url = "https://www.allow-url-example.com"
    vastResult = VastValidator().test(vpc)

    vastResult.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_placement_domain_list_allow_negative():
    case = Case("test_placement_domain_list_allow_negative")

    vpc = case.vpc
    vpc.page_url = "https://www.not-allow-url-example.com"
    vastResult = VastValidator().test(vpc)

    vastResult.assertFilter(FilterReason.PUBLISHER_FILTER)

    vastResult.assertXML().assertAdsCount(0)
