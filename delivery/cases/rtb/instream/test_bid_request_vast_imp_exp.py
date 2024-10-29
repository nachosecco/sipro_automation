import pytest

from core.case import Case
from core.vastValidator import VastValidator


def validate_rtb_ctv_common_properties(bid_request_validator, case_name):
    assert bid_request_validator.is_placement_type_as_expected("vast")
    assert bid_request_validator.is_required_properties_valid()
    assert bid_request_validator.is_allimps_as_expected(0)


def get_expected_imp_object_rtb24():
    expected_imp = [
        {
            "id": "1",
            "video": {
                "mimes": ["video/mp4", "video/3gpp", "video/webm"],
                "minduration": 5,
                "maxduration": 60,
                "protocols": [7, 8, 3, 6, 2, 5],
                "w": 640,
                "h": 480,
                "startdelay": 0,
                "linearity": 1,
                "sequence": 0,
                "maxextended": 30,
                "minbitrate": 300,
                "maxbitrate": 25000,
                "delivery": [1, 2, 3],
                "pos": 1,
                "api": [],
                "skip": 0,
            },
            "instl": 0,
            "bidfloor": 0.01,
            "bidfloorcur": "USD",
            "secure": 1,
            "exp": 300,
            "ext": {"ssai": 0},
        }
    ]
    return expected_imp


def get_expected_imp_object_rtb25():
    expected_imp = [
        {
            "id": "1",
            "video": {
                "mimes": ["video/mp4", "video/3gpp", "video/webm"],
                "minduration": 5,
                "maxduration": 60,
                "protocols": [7, 8, 3, 6, 2, 5],
                "w": 640,
                "h": 480,
                "startdelay": 0,
                "placement": 1,
                "linearity": 1,
                "sequence": 0,
                "maxextended": 30,
                "minbitrate": 300,
                "maxbitrate": 25000,
                "playbackend": 1,
                "delivery": [1, 2, 3],
                "pos": 1,
                "api": [],
                "skip": 0,
                "plcmt": 1,
            },
            "instl": 0,
            "bidfloor": 0.01,
            "bidfloorcur": "USD",
            "secure": 1,
            "exp": 300,
            "ext": {"ssai": 0},
        }
    ]
    return expected_imp


def get_expected_imp_object_rtb26():
    expected_imp = get_expected_imp_object_rtb25()
    expected_imp[0]["ssai"] = 0
    expected_imp[0]["ext"] = {}
    return expected_imp


# Test RTB 2.4 bid request for CTV placement


@pytest.mark.regression
def test_bid_request_vast_imp_exp_rtb24():
    case = Case(
        "test_bid_request_vast_imp_exp_rtb24"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.page_url = "siprocal.com"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_vast_imp_exp_rtb24"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_vast_imp_exp_rtb24"
    )

    assert bid_request_validator.is_imp_object_as_expected(
        get_expected_imp_object_rtb24()
    )


# Test RTB 2.5 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_vast_imp_exp_rtb25():
    case = Case(
        "test_bid_request_vast_imp_exp_rtb25"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.page_url = "siprocal.com"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_vast_imp_exp_rtb25"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_vast_imp_exp_rtb25"
    )

    assert bid_request_validator.is_imp_object_as_expected(
        get_expected_imp_object_rtb25()
    )


# Test RTB 2.6 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_vast_imp_exp_rtb26():
    case = Case(
        "test_bid_request_vast_imp_exp_rtb26"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.page_url = "siprocal.com"

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_vast_imp_exp_rtb26"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_vast_imp_exp_rtb26"
    )

    assert bid_request_validator.is_imp_object_as_expected(
        get_expected_imp_object_rtb26()
    )
