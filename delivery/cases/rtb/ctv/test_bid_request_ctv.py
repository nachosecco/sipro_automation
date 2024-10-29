import pytest
from core.case import Case
from core.configuration import Configuration

from core.vastValidator import VastValidator


def validate_rtb_ctv_common_properties(bid_request_validator, case_name):
    assert bid_request_validator.is_placement_type_as_expected("mobile")
    assert bid_request_validator.is_required_properties_valid()
    assert bid_request_validator.is_video_object_valid()
    assert bid_request_validator.is_app_object_valid()
    assert bid_request_validator.is_app_object_as_expected(case_name)
    expected_regs = {"coppa": 0, "ext": {"gdpr": 0, "us_privacy": "1---"}}
    assert bid_request_validator.is_regs_object_as_expected(expected_regs)
    assert bid_request_validator.is_tmax_as_expected(Configuration().rtb_tmax)
    assert bid_request_validator.is_at_as_expected(2)
    assert bid_request_validator.is_allimps_as_expected(0)
    assert bid_request_validator.is_cur_as_expected(["USD"])


def get_expected_device_object_rtb22():
    expected_device = {
        "ua": "REPLACE",
        "geo": {
            "country": "[REPLACE]",
            "region": "[REPLACE]",
            "metro": "[REPLACE]",
            "city": "",
            "zip": "[REPLACE]",
            "type": 2,
        },
        "dnt": 0,
        "ip": "REPLACE",
        "os": "Other",
        "js": 0,
        "connectiontype": 0,
        "ifa": "REPLACE",
    }
    return expected_device


def get_expected_user_object_rtb22():
    expected_user = {
        "geo": {
            "country": "[REPLACE]",
            "region": "[REPLACE]",
            "metro": "[REPLACE]",
            "city": "",
            "zip": "[REPLACE]",
            "type": 2,
        },
		"ext": {}
    }
    return expected_user


def get_expected_imp_object_rtb22():
    expected_imp = [
        {
            "id": "REPLACE",
            "video": {
                "mimes": ["video/mp4", "video/3gpp", "video/webm"],
                "minduration": 5,
                "maxduration": 60,
                "protocols": [2, 5],
                "w": 640,
                "h": 480,
                "linearity": 1,
                "sequence": 0,
                "maxextended": 30,
                "minbitrate": 300,
                "maxbitrate": 25000,
                "delivery": [1, 2, 3],
                "pos": 1,
                "api": [],
            },
            "instl": 0,
            "tagid": "REPLACE",
            "bidfloor": 0.01,
            "bidfloorcur": "USD",
            "secure": 1,
            "ext": {"ssai": 0},
        }
    ]
    return expected_imp


# Returns expected Ext object as specified in RTB 2.2 in test bid requests
def get_expected_ext_object_rtb22(root_domain):
    expected_ext = {
        "schain": {
            "ver": "1.0",
            "complete": 1,
            "nodes": [
                {
                    "asi": root_domain,
                    "sid": "REPLACE",
                    "hp": 1,
                    "rid": "REPLACE",
                }
            ],
        }
    }
    return expected_ext


# Test RTB 2.2 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_rtb22():
    root_domain = Configuration().root_domain
    case = Case("test_bid_request_ctv_rtb22")  # This is the file to test this case

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_rtb22"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_rtb22"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb22()
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb22())
    assert bid_request_validator.is_imp_object_as_expected(
        get_expected_imp_object_rtb22()
    )
    assert bid_request_validator.is_ext_object_as_expected(
        get_expected_ext_object_rtb22(root_domain)
    )


def get_expected_device_object_rtb23():
    expected_device = get_expected_device_object_rtb22()
    expected_device["lmt"] = 0
    return expected_device


# Test RTB 2.3 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_rtb23():
    root_domain = Configuration().root_domain
    case = Case("test_bid_request_ctv_rtb23")  # This is the file to test this case

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_rtb23"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_rtb23"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb23()
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb22())
    assert bid_request_validator.is_imp_object_as_expected(
        get_expected_imp_object_rtb22()
    )
    assert bid_request_validator.is_ext_object_as_expected(
        get_expected_ext_object_rtb22(root_domain)
    )


def get_expected_device_object_rtb24():
    expected_device = get_expected_device_object_rtb23()
    expected_device["geo"]["ipservice"] = 3
    expected_device["geofetch"] = 0
    return expected_device


def get_expected_user_object_rtb24():
    expected_user = get_expected_user_object_rtb22()
    expected_user["geo"]["ipservice"] = 3
    return expected_user


def get_expected_imp_object_rtb24():
    expected_imp = get_expected_imp_object_rtb22()
    expected_imp[0].get("video", None)["skip"] = 0
    return expected_imp


# Test RTB 2.4 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_rtb24():
    root_domain = Configuration().root_domain
    case = Case("test_bid_request_ctv_rtb24")  # This is the file to test this case

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_rtb24"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_rtb24"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24()
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb24())
    assert bid_request_validator.is_imp_object_as_expected(
        get_expected_imp_object_rtb24()
    )
    assert bid_request_validator.is_ext_object_as_expected(
        get_expected_ext_object_rtb22(root_domain)
    )


def get_expected_imp_object_rtb25():
    expected_imp = get_expected_imp_object_rtb24()
    video = expected_imp[0]["video"]
    video["placement"] = 1
    video["plcmt"] = 1
    video["playbackend"] = 1
    return expected_imp


def get_expected_source_object_rtb25(root_domain):
    expected_source = {
        "fd": 0,
        "tid": "REPLACE",
        "ext": {
            "schain": {
                "ver": "1.0",
                "complete": 1,
                "nodes": [
                    {
                        "asi": root_domain,
                        "sid": "REPLACE",
                        "hp": 1,
                        "rid": "REPLACE",
                    }
                ],
            }
        },
    }
    return expected_source


# Test RTB 2.5 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_rtb25():
    root_domain = Configuration().root_domain
    case = Case("test_bid_request_ctv_rtb25")  # This is the file to test this case

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_rtb25"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_rtb25"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24()
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb24())
    assert bid_request_validator.is_imp_object_as_expected(
        get_expected_imp_object_rtb25()
    )
    assert bid_request_validator.is_source_object_as_expected(
        get_expected_source_object_rtb25(root_domain)
    )


def get_expected_imp_object_rtb26():
    expected_imp = get_expected_imp_object_rtb25()
    expected_imp[0]["ssai"] = 0
    expected_imp[0]["ext"] = {}
    return expected_imp


# Test RTB 2.6 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_rtb26():
    root_domain = Configuration().root_domain
    case = Case("test_bid_request_ctv_rtb26")  # This is the file to test this case

    vpc = case.vpc

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_rtb26"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_rtb26"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24()
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb24())
    assert bid_request_validator.is_imp_object_as_expected(
        get_expected_imp_object_rtb26()
    )
    assert bid_request_validator.is_source_object_as_expected(
        get_expected_source_object_rtb25(root_domain)
    )
