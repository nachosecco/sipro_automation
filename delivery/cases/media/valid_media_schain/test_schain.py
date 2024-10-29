from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator
from core.constants import ComparisonType
import pytest

from core.configuration import Configuration


@pytest.mark.regression
@description(
    """test that a valid schain parameter is passed is a valid in vpc request"""
)
def test_schain_query_param():
    case = Case("test_schain_query_param")
    vpc = case.vpc
    vpc.schain = "12345"
    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    vast_result.assertLogsDelivery(["schain=12345"])


@pytest.mark.regression
@description(
    """test that a valid schain parameter is passed
    through in the media tag with our account information appended"""
)
def test_valid_schain_tag():
    case = Case("test_valid_schain_tag")
    ads_txt_account_id = case.data_environment.supply().publisher.adsTxtAccountId
    vpc = case.vpc
    schain_version = "1.0"
    schain_complete = "1"
    domain = Configuration().root_domain
    referer_domain = "disney.com"
    referer_account_id = "ads-disney"

    vpc.schain = f"{schain_version},{schain_complete}!{referer_domain},{referer_account_id},{schain_complete}"

    expected_schain_placement = f"!{domain},{ads_txt_account_id},{schain_complete}"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)
    assert_media_tags = vast_result.assertXML().assertMediaTags()
    expected_schain = vpc.schain + expected_schain_placement
    assert_media_tags.ad_tag("schain", expected_schain, ComparisonType.Equality)
    vast_result.assertCase(case)


@pytest.mark.regression
@description(
    """test that a valid schain parameter is passed is a invalid
    through in the media tag with our account information appended"""
)
def test_invalid_schain_tag():
    case = Case("test_invalid_schain_tag")  # This is the file to test this case
    ads_txt_account_id = case.data_environment.supply().publisher.adsTxtAccountId
    root_domain = Configuration().root_domain
    vpc = case.vpc
    vpc.schain = f"1.0,1!{root_domain},{ads_txt_account_id},2"
    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)
    assert_media_tags = vast_result.assertXML().assertMediaTags()
    assert_media_tags.ad_tag(
        "schain",
        f"1.0,1!{root_domain},{ads_txt_account_id},1",
        ComparisonType.Equality,
    )
    # This will execute the all assertions in the case
    vast_result.assertCase(case)


# validating the schain value is empty check in the vast response (VASTAdTagURI)
@pytest.mark.regression
def test_empty_schain_tag():
    case = Case("test_empty_schain_tag")
    ads_txt_account_id = case.data_environment.supply().publisher.adsTxtAccountId
    root_domain = Configuration().root_domain
    vpc = case.vpc
    # This would execute the framework
    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)
    assert_media_tags = vast_result.assertXML().assertMediaTags()
    assert_media_tags.ad_tag(
        "schain",
        f"1.0,1!{root_domain},{ads_txt_account_id},1",
        ComparisonType.Equality,
    )
    vast_result.assertCase(case)
