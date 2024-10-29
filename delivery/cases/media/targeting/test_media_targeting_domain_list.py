import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason
from core.configuration import Configuration
import copy


@pytest.mark.regression
def test_media_domain_list_block():
    case = Case("test_media_domain_list_block")

    vpc = case.vpc
    vpc.page_url = "https://www.blocked-url-example.com"
    vastResult = VastValidator().test(vpc)

    vastResult.assertFilter(FilterReason.TARGETING_DOMAIN)

    vastResult.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_media_domain_list_block_negative():
    case = Case("test_media_domain_list_block_negative")

    vpc = case.vpc
    vpc.page_url = "https://www.not-blocked-url-example.com"

    vastResult = VastValidator().test(vpc)

    vastResult.assertXML().assertAdsCount(1)


# adding this test for not run for now , this test always passed from local run but sometime failed from Jenkins . untill find the root cuase skiping this test
@pytest.mark.regressionSKIP
def test_media_domain_list_allow():
    case = Case("test_media_domain_list_allow")
    configOverride: Configuration = copy.deepcopy(Configuration())
    configOverride.open_search_time_to_wait_to_read_delivery_tid = 20
    configOverride.open_search_time_to_wait_to_read_delivery = 20

    vpc = case.vpc
    vpc.page_url = "https://www.allow-url-example.com"
    vastResult = VastValidator().test(vpc)

    vastResult.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_media_domain_list_allow_negative():
    case = Case("test_media_domain_list_allow_negative")

    vpc = case.vpc
    vpc.page_url = "https://www.not-allow-url-example.com"
    vastResult = VastValidator().test(vpc)

    vastResult.assertFilter(FilterReason.TARGETING_DOMAIN)

    vastResult.assertXML().assertAdsCount(0)
