import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_dynamic_media_extension_adomain():
    """
    This test case uses programmatic demand with bidder url to fakebidder which returns bid response including list of advertiser domains.
    Expected result: the vast response should contain the Adomain extension
    """
    case = Case("test_dynamic_media_extension_adomain")

    vpc = case.vpc
    vpc.min_price = "1"
    vpc.use_dynamic_pricing = "true"
    VastValidator().test(vpc).assert_extension().assert_adomain(
        1, "https://www.smaato.com"
    )


@pytest.mark.regression
def test_dynamic_media_extension_with_two_adomains():
    """
    This test case uses programmatic demand with bidder url to fakebidder which returns bid response including list of two advertiser domains.
    Expected result: the vast response should contain the Adomain extension with two adomain tags
    """

    case = Case("test_dynamic_media_extension_with_two_adomains")

    vpc = case.vpc
    vpc.min_price = "1"
    vpc.use_dynamic_pricing = "true"
    VastValidator().test(vpc).assert_extension().assert_adomain(
        1, "https://www.test.com"
    )

    VastValidator().test(vpc).assert_extension().assert_adomain(2, "google.com")
