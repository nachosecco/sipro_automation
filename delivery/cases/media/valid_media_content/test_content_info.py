import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.constants import ComparisonType, REPLACE


# validating content episode in vast response
@pytest.mark.regression
def test_media_ad_tag_content_info():
    case = Case("test_media_ad_tag_content_info")  # This is the file to test this case

    vpc = case.vpc
    vpc.content_episode = "5"
    vpc.content_title = "Star Wars"
    vpc.content_series = "The Office"
    vpc.content_genre = "Comedy, Drama"
    vpc.content_cat = "IAB_1_7"
    vpc.content_prodq = "1"
    vpc.content_qagmediarating = "2"
    vpc.content_livestream = "0"
    vpc.content_len = "180"
    vpc.content_language = "eng"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag(
        "content_episode", vpc.content_episode, ComparisonType.Equality
    )
    assertMediaTags.ad_tag("content_title", vpc.content_title, ComparisonType.Equality)
    assertMediaTags.ad_tag(
        "content_series", vpc.content_series, ComparisonType.Equality
    )
    assertMediaTags.ad_tag("content_genre", vpc.content_genre, ComparisonType.Equality)
    assertMediaTags.ad_tag("content_cat", vpc.content_cat, ComparisonType.Equality)
    assertMediaTags.ad_tag("content_prodq", vpc.content_prodq, ComparisonType.Equality)
    assertMediaTags.ad_tag(
        "content_qagmediarating", vpc.content_qagmediarating, ComparisonType.Equality
    )
    assertMediaTags.ad_tag(
        "content_livestream", vpc.content_livestream, ComparisonType.Equality
    )
    assertMediaTags.ad_tag("content_len", vpc.content_len, ComparisonType.Equality)
    assertMediaTags.ad_tag(
        "content_language", vpc.content_language, ComparisonType.Equality
    )


@pytest.mark.regression
def test_media_ad_tag_content_empty_info():
    case = Case("test_media_ad_tag_content_empty_info")
    vpc = case.vpc
    vastResult = VastValidator().test(vpc)

    vastResult.assertCase(case)

    assertMediaTags = vastResult.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("content_episode", "")
    assertMediaTags.ad_tag("content_title", REPLACE)
    assertMediaTags.ad_tag("content_series", REPLACE)
    assertMediaTags.ad_tag("content_genre", REPLACE)
    assertMediaTags.ad_tag("content_cat", "")
    assertMediaTags.ad_tag("content_prodq", "")
    assertMediaTags.ad_tag("content_qagmediarating", "")
    assertMediaTags.ad_tag("content_livestream", "")
    assertMediaTags.ad_tag("content_len", "")
    assertMediaTags.ad_tag("content_language", REPLACE)
