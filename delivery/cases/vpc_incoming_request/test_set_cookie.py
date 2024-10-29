import pytest

from core.Description import description
from core.case import Case
from core.vastValidator import VastValidator


# If we don't send user id data (cookie or device) and is not opted out, and is a web invocation it should set a cookie
# after invocation
@pytest.mark.regression
def test_when_no_cid_idfa_advid_did_didtype_should_set_usercookie():
    # The scenario invokes delivery with no cid, idfa, adv_id, did or did_type parameter
    case = Case("test_cookie_setting")
    vpc = case.vpc
    vpc.did = ""
    vpc.cid = ""
    vpc.did_type = ""
    vpc.idfa = ""
    vpc.adv_id = ""

    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    vast_result.validate_headers().assert_header_nonempty("Set-Cookie")
    vast_result.validate_headers().assert_header_value("Set-Cookie", "ALT_UC748")


@pytest.mark.regression
def test_when_cid_should_no_set_usercookie():
    # The scenario invokes delivery with cid parameter
    case = Case("test_cookie_setting")
    vpc = case.vpc
    vpc.cid = "4CA6P8KRPC8UP5660DRAB74EMG"
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    vast_result.validate_headers().assert_header_not_present("Set-Cookie")


@pytest.mark.regression
def test_when_did_should_no_set_usercookie():
    # The scenario invokes delivery with cid parameter
    case = Case("test_cookie_setting")
    vpc = case.vpc
    vpc.did = "00000000-89ABCDEF-01234567-89ABCDEF"
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)
    vast_result.validate_headers().assert_header_not_present("Set-Cookie")


@pytest.mark.regression
@description(
    """When a placement of Instream type have value 1 for Do Not Track tag, it should not return user cookies in
    response Header"""
)
def test_when_dnt_set_one_should_no_set_usercookie():
    # The scenario invokes delivery with dnt parameter as 1
    case = Case("test_when_dnt_set_one_should_no_set_usercookie")
    vpc = case.vpc
    vpc.dnt = "1"
    vpc.did = ""
    vpc.did_type = ""
    vpc.page_url = "page_url"
    vast_result = VastValidator().test(vpc)
    vast_result.validate_headers().assert_header_not_present("Set-Cookie")
