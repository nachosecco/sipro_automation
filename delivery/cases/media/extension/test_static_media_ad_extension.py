import pytest
from core.case import Case
from core.vastValidator import VastValidator


@pytest.mark.regression
def test_media_extension_adomain_wrapper_vast():
    """
    This test case uses media with "ford.com" advertiser domain and aligned to a placement.
    Expected result: the vast response should contain the Adomain extension xml tag in the wrapper ad
    """
    case = Case("test_media_extension_adomain_wrapper_vast")

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "0.01"

    VastValidator().test(vpc).assert_extension().assert_adomain("1", "ford.com")


@pytest.mark.regression
def test_media_extension_adomain_wrapper_vast_missing():
    """
    This test case uses media with empty advertiser domain and aligned to a placement.
    Expected result: the vast response should not contain the Adomain extension xml tag in the wrapper ad
    """
    case = Case("test_media_extension_adomain_wrapper_vast_missing")

    vpc = case.vpc
    VastValidator().test(vpc).assert_extension().assert_noAdomain()


@pytest.mark.regression
def test_media_extension_adomain_inline_vast():
    """
    This test case uses media with "abc.com" advertiser domain and aligned to a placement.
    Expected result: the vast response should contain the Adomain extension xml tag in the inline ad
    """
    case = Case("test_media_extension_adomain_inline_vast")

    vpc = case.vpc

    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "0.01"

    VastValidator().test(vpc).assert_extension().assert_adomain("1", "abc.com")


@pytest.mark.regression
def test_media_extension_adomain_inline_vast_missing():
    """
    This test case uses media with empty advertiser domain and aligned to a placement.
    Expected result: the vast response should not contain the Adomain extension xml tag in the inline ad
    """
    case = Case("test_media_extension_adomain_inline_vast_missing")

    vpc = case.vpc
    vpc.use_dynamic_pricing = "true"
    vpc.min_price = "0.01"
    VastValidator().test(vpc).assert_extension().assert_noAdomain()
