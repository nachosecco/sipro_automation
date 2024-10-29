import pytest
from core.case import Case
from core.configuration import Configuration
from core.constants import PYTHON_REQUEST_UA
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo, get_geo_for_ip


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


def get_expected_device_object_rtb22(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_device = {
        "ua": f"{PYTHON_REQUEST_UA}",
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "MEX",
            "region": "JAL",
            "metro": "",
            "city": "Guadalajara",
            "zip": "44900",
            "type": 2,
        },
        "dnt": 0,
        "ip": ip_address,
        "os": "Other",
        "js": 0,
        "carrier": geo_data["carrier"],
        "connectiontype": geo_data["connection_type_code"],
        "ifa": "fe088fc1-4cb4-548e-989b-6f8ff834e27d",
    }
    return expected_device


def get_expected_user_object_rtb22(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_user = {
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "MEX",
            "region": "JAL",
            "metro": "",
            "city": "Guadalajara",
            "zip": "44900",
            "type": 2,
        },
		"ext": {}
    }
    return expected_user


# Test RTB 2.2 bid request for CTV placement geo targeting country Mexico state Jalisco
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb22_country_mexico_state_jalisco_valid():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb22_country_mexico_state_jalisco_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_ctv_rtb22_country_mexico_state_jalisco_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_ctv_rtb22_country_mexico_state_jalisco_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb22(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb22(vpc.ip_address)
    )


def get_expected_device_object_rtb23(ip_address):
    expected_device = get_expected_device_object_rtb22(ip_address)
    expected_device["geo"]["utcoffset"] = -360
    expected_device["lmt"] = 0
    return expected_device


def get_expected_user_object_rtb23(ip_address):
    expected_user = get_expected_user_object_rtb22(ip_address)
    expected_user["geo"]["utcoffset"] = -360
    return expected_user


# Test RTB 2.3 bid request for CTV placement geo targeting country Mexico state Jalisco
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb23_country_mexico_state_jalisco_valid():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb23_country_mexico_state_jalisco_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_ctv_rtb23_country_mexico_state_jalisco_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_ctv_rtb23_country_mexico_state_jalisco_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb23(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb23(vpc.ip_address)
    )


def get_expected_device_object_rtb24(ip_address):
    expected_device = get_expected_device_object_rtb23(ip_address)
    expected_device["geo"]["ipservice"] = 3
    expected_device["geofetch"] = 0
    return expected_device


def get_expected_user_object_rtb24(ip_address):
    expected_user = get_expected_user_object_rtb23(ip_address)
    expected_user["geo"]["ipservice"] = 3
    return expected_user


# Test RTB 2.4 bid request for CTV placement geo targeting country Mexico state Jalisco
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb24_country_mexico_state_jalisco_valid():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb24_country_mexico_state_jalisco_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_ctv_rtb24_country_mexico_state_jalisco_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_ctv_rtb24_country_mexico_state_jalisco_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.5 bid request for CTV placement geo targeting country Mexico state Jalisco
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb25_country_mexico_state_jalisco_valid():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb25_country_mexico_state_jalisco_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_ctv_rtb25_country_mexico_state_jalisco_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_ctv_rtb25_country_mexico_state_jalisco_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.6 bid request for CTV placement geo targeting country Mexico state Jalisco
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb26_country_mexico_state_jalisco_valid():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb26_country_mexico_state_jalisco_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_ctv_rtb26_country_mexico_state_jalisco_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_ctv_rtb26_country_mexico_state_jalisco_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.2 bid request for CTV placement geo targeting country Mexico state Jalisco negative
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb22_country_mexico_state_jalisco_negative():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb22_country_mexico_state_jalisco_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.3 bid request for CTV placement geo targeting country Mexico state Jalisco negative
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb23_country_mexico_state_jalisco_negative():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb23_country_mexico_state_jalisco_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.4 bid request for CTV placement geo targeting country Mexico state Jalisco negative
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb24_country_mexico_state_jalisco_negative():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb24_country_mexico_state_jalisco_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.5 bid request for CTV placement geo targeting country Mexico state Jalisco negative
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb25_country_mexico_state_jalisco_negative():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb25_country_mexico_state_jalisco_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.6 bid request for CTV placement geo targeting country Mexico state Jalisco negative
@pytest.mark.regression
def test_bid_request_geo_targeting_ctv_rtb26_country_mexico_state_jalisco_negative():
    case = Case(
        "test_bid_request_geo_targeting_ctv_rtb26_country_mexico_state_jalisco_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="MX", region="Jalisco", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)
    # Validate the VAST Response

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)
