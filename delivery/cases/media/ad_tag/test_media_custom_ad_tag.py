import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.constants import NOT_FOUND


# Configuration - A placement with an aligned media. Media is configured with custom tags c1 & c2.
@pytest.mark.regression
def test_media_custom_ad_tag_values_passed():
    case = Case("test_media_custom_ad_tag_values_passed")
    vpc = case.vpc
    vpc.custom_tags = {"c1": "test1", "c2": "test2"}
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)
    assert_media_tags = vast_result.assertXML().assertMediaTags()
    assert_media_tags.ad_tag("c1", vpc.custom_tags.get("c1"))
    assert_media_tags.ad_tag("c2", vpc.custom_tags.get("c2"))


# Configuration - A placement with an aligned media. Media is configured with custom tags c1 & c2.
@pytest.mark.regression
def test_media_custom_ad_tag_partial_values_passed():
    case = Case("test_media_custom_ad_tag_partial_values_passed")
    vpc = case.vpc
    vpc.custom_tags = {"c1": "test1"}
    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)
    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("c1", vpc.custom_tags.get("c1"))
    assertMediaTags.ad_tag("c2", NOT_FOUND)


# Configuration - A placement with an aligned media. Media is configured with custom tags c1 & c2.
@pytest.mark.regression
def test_media_custom_ad_tag_no_values_passed():
    case = Case("test_media_custom_ad_tag_no_values_passed")
    vpc = case.vpc
    vpc.custom_tags = {}
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("c1", NOT_FOUND)
