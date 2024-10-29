import pytest
from core.case import Case

from core.Description import description
from core.vastValidator import VastValidator


@description(
    "Tests media tags has value when provided. Placement has aligned media with tags gpp and gpp_sid."
    "Media Tag: <Media URL>?gpp=[gpp]&gpp_sid=[gpp_sid]"
)
@pytest.mark.regression
def test_gpp_and_gpp_sid_tag():
    case = Case("test_gpp_and_gpp_sid_tag")
    vpc = case.vpc
    vpc.gpp = "DBABRg~BQAAABA"
    vpc.gpp_sid = "9"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    assertMediaTags = vast_result.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("gpp", "DBABRg~BQAAABA")
    assertMediaTags.ad_tag("gpp_sid", "9")


@description(
    "Tests media tags are empty when not found. Placement has aligned media with tags gpp and gpp_sid."
    "Media Tag: <Media URL>?gpp=[gpp]&gpp_sid=[gpp_sid]"
)
@pytest.mark.regression
def test_missing_gpp_and_gpp_sid_tag():
    case = Case("test_missing_gpp_and_gpp_sid_tag")

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    assertMediaTags = vast_result.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("gpp", "")
    assertMediaTags.ad_tag("gpp_sid", "")


@description(
    "Tests media tags are empty when gpp_sid is missing. Placement has aligned media with tags gpp and "
    "gpp_sid."
    "Media Tag: <Media URL>?gpp=[gpp]&gpp_sid=[gpp_sid]"
)
@pytest.mark.regression
def test_missing_gpp_sid_tag():
    case = Case("test_missing_gpp_sid_tag")

    vpc = case.vpc
    vpc.gpp = "DBABRg~BQAAABA"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    assertMediaTags = vast_result.assertXML().assertMediaTags()
    assertMediaTags.ad_tag("gpp", "")
    assertMediaTags.ad_tag("gpp_sid", "")
