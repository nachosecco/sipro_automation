import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_ad_tag_page_info_valid_values():
    case = Case("test_media_ad_tag_page_info_valid_values")
    vpc = case.vpc
    vpc.page_url = "pageurl.com"
    vpc.page_domain = "pagedomain"
    vpc.ref_page_url = "refpageurl.com"
    vpc.ref_page_domain = "refdomain"
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("page_url", vpc.page_url)
    assertMediaTags.ad_tag("page_domain", vpc.page_url)
    assertMediaTags.ad_tag("ref_page_url", vpc.ref_page_url)
    assertMediaTags.ad_tag("ref_page_domain", vpc.ref_page_url)


@pytest.mark.regression
def test_media_ad_tag_page_info_empty_values():
    case = Case("test_media_ad_tag_page_info_empty_values")
    vpc = case.vpc
    vpc.page_url = "pageurl.com"

    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("page_url", vpc.page_url)
    assertMediaTags.ad_tag("page_domain", vpc.page_url)
    assertMediaTags.ad_tag("ref_page_url", "")
    assertMediaTags.ad_tag("ref_page_domain", "")
