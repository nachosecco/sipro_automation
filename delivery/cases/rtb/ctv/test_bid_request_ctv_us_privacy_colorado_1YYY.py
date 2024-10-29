import pytest
from core.case import Case
from core.configuration import Configuration
from core.utils.geoIpUtils import get_ip_for_geo
from core.vastValidator import VastValidator


def validate_rtb_ctv_common_properties(bid_request_validator, case_name):
    assert bid_request_validator.is_placement_type_as_expected("mobile")
    assert bid_request_validator.is_required_properties_valid()
    assert bid_request_validator.is_video_object_valid()
    assert bid_request_validator.is_app_object_valid()
    assert bid_request_validator.is_app_object_as_expected(case_name)
    expected_regs = {"coppa": 0, "ext": {"gdpr": 0, "us_privacy": "1YYY"}}
    assert bid_request_validator.is_regs_object_as_expected(expected_regs)
    assert bid_request_validator.is_number_of_properties_as_expected(11)
    assert bid_request_validator.is_tmax_as_expected(Configuration().rtb_tmax)
    assert bid_request_validator.is_at_as_expected(2)
    assert bid_request_validator.is_allimps_as_expected(0)
    assert bid_request_validator.is_cur_as_expected(["USD"])


def get_expected_device_object_rtb22():
    expected_device = {
        "geo": {},
        "dnt": 0,
        "os": "Other",
        "js": 0,
        "connectiontype": 0,
    }
    return expected_device


def get_expected_user_object_rtb22():
    expected_user = {"geo": {}, "ext": {}}
    return expected_user


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
def test_bid_request_ctv_us_privacy_colorado_1YYY_rtb22():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb22"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1YYY"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb22"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb22"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb22(), True
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb22())
    assert bid_request_validator.is_ext_object_as_expected(
        get_expected_ext_object_rtb22(root_domain)
    )


def get_expected_device_object_rtb23():
    expected_device = {
        "geo": {},
        "dnt": 0,
        "lmt": 0,
        "os": "Other",
        "js": 0,
        "connectiontype": 0,
    }
    return expected_device


# Test RTB 2.3 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_us_privacy_colorado_1YYY_rtb23():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb23"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1YYY"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb23"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb23"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb23(), True
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb22())
    assert bid_request_validator.is_ext_object_as_expected(
        get_expected_ext_object_rtb22(root_domain)
    )


def get_expected_device_object_rtb24():
    expected_device = get_expected_device_object_rtb23()
    expected_device["geofetch"] = 0
    return expected_device


def get_expected_user_object_rtb24():
    expected_user = get_expected_user_object_rtb22()
    return expected_user


# Test RTB 2.4 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_us_privacy_colorado_1YYY_rtb24():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb24"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1YYY"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb24"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb24"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(), True
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb24())
    assert bid_request_validator.is_ext_object_as_expected(
        get_expected_ext_object_rtb22(root_domain)
    )


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
def test_bid_request_ctv_us_privacy_colorado_1YYY_rtb25():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb25"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1YYY"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb25"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb25"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(), True
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb24())
    assert bid_request_validator.is_source_object_as_expected(
        get_expected_source_object_rtb25(root_domain)
    )


# Test RTB 2.6 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_us_privacy_colorado_1YYY_rtb26():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb26"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1YYY"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(country="US", region="Colorado")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb26"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1YYY_rtb26"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(), True
    )
    assert bid_request_validator.is_user_as_expected(get_expected_user_object_rtb24())
    assert bid_request_validator.is_source_object_as_expected(
        get_expected_source_object_rtb25(root_domain)
    )
