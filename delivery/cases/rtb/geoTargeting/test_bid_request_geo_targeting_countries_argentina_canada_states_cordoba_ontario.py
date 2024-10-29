import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.configuration import Configuration
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
        "ua": "python-requests/2.28.1",
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "ARG",
            "region": "X",
            "metro": "",
            "city": "Villa del Rosario",
            "zip": "5963",
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
            "country": "ARG",
            "region": "X",
            "metro": "",
            "city": "Villa del Rosario",
            "zip": "5963",
            "type": 2,
        },
		"ext": {}
    }

    return expected_user


# Test RTB 2.2 bid request for geo targeting country argentina state cordoba.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb22_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb22_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "AR"
    geo.regionName = "Cordoba"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that there is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb22_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb22_valid",
    )
    # Validating the Device Object
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb22(vpc.ip_address)
    )
    # Validating the User Object
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb22(vpc.ip_address)
    )


def get_expected_device_object_rtb23(ip_address):
    expected_device = get_expected_device_object_rtb22(ip_address)
    expected_device["geo"]["utcoffset"] = -180
    expected_device["lmt"] = 0
    return expected_device


def get_expected_user_object_rtb23(ip_address):
    expected_user = get_expected_user_object_rtb22(ip_address)
    expected_user["geo"]["utcoffset"] = -180
    return expected_user


# Test RTB 2.3 bid request for CTV placement geo targeting country argentina state cordoba.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb23_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb23_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
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
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb23_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb23_valid",
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


# Test RTB 2.4 bid request for CTV placement geo targeting country argentina state cordoba.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb24_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb24_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
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
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb24_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb24_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.5 bid request for CTV placement country argentina state cordoba.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb25_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb25_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
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
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb25_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb25_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.6 bid request for CTV placement geo targeting country argentina state cordoba.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb26_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb26_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
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
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb26_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb26_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.2 bid request for CTV placement geo targeting country argentina state cordoba negative
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb22_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb22_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.3 bid request for CTV placement geo targeting country argentina state cordoba negative
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb23_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb23_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.4 bid request for CTV placement geo targeting country argentina state cordoba negative
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb24_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb24_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.5 bid request for CTV placement geo targeting country argentina state cordoba negative
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb25_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb25_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.6 bid request for CTV placement geo targeting country argentina state cordoba negative
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb26_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_argentina_states_cordoba_rtb26_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)
    # Validate the VAST Response

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# canada device object
def get_canada_expected_device_object_rtb22(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_device = {
        "ua": "python-requests/2.28.0",
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "CAN",
            "region": "ON",
            "metro": "",
            "city": "Toronto",
            "zip": "M6H",
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


# canada user object
def get_canada_expected_user_object_rtb22(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_user = {
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "CAN",
            "region": "ON",
            "metro": "",
            "city": "Toronto",
            "zip": "M6H",
            "type": 2,
        },
		"ext": {}
    }
    return expected_user


# Test RTB 2.2 bid request for geo targeting country canada state ontario.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb22_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb22_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "CA"
    geo.regionName = "Ontario"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that there is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb22_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb22_valid",
    )
    # Validating the Device Object
    assert bid_request_validator.is_device_object_as_expected(
        get_canada_expected_device_object_rtb22(vpc.ip_address)
    )
    # Validating the User Object
    assert bid_request_validator.is_user_as_expected(
        get_canada_expected_user_object_rtb22(vpc.ip_address)
    )


def get_canada_expected_device_object_rtb23(ip_address):
    expected_device = get_canada_expected_device_object_rtb22(ip_address)
    expected_device["geo"]["utcoffset"] = -300
    expected_device["lmt"] = 0
    return expected_device


def get_canada_expected_user_object_rtb23(ip_address):
    expected_user = get_canada_expected_user_object_rtb22(ip_address)
    expected_user["geo"]["utcoffset"] = -300
    return expected_user


# Test RTB 2.3 bid request for CTV placement geo targeting country canada state ontario.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb23_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb23_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
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
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb23_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb23_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_canada_expected_device_object_rtb23(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_canada_expected_user_object_rtb23(vpc.ip_address)
    )


def get_canada_expected_device_object_rtb24(ip_address):
    expected_device = get_canada_expected_device_object_rtb23(ip_address)
    expected_device["geo"]["ipservice"] = 3
    expected_device["geofetch"] = 0
    return expected_device


def get_canada_expected_user_object_rtb24(ip_address):
    expected_user = get_canada_expected_user_object_rtb23(ip_address)
    expected_user["geo"]["ipservice"] = 3
    return expected_user


# Test RTB 2.4 bid request for CTV placement geo targeting country canada state ontario.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb24_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb24_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
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
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb24_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb24_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_canada_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_canada_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.5 bid request for CTV placement geo targeting country canada state ontario.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb25_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb25_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
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
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb25_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb25_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_canada_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_canada_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.6 bid request for CTV placement geo targeting country canada state ontario.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb26_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb26_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
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
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb26_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb26_valid",
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_canada_expected_device_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_user_as_expected(
        get_canada_expected_user_object_rtb24(vpc.ip_address)
    )


# Test RTB 2.2 bid request for CTV placement geo targeting country canada state ontario negative.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb22_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb22_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.3 bid request for CTV placement geo targeting country canada state ontario negative.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb23_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb23_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.4 bid request for CTV placement geo targeting country canada state ontario negative.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb24_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb24_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.5 bid request for CTV placement geo targeting country canada state ontario negative.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb25_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb25_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)


# Test RTB 2.6 bid request for CTV placement geo targeting country canada state ontario negative.
@pytest.mark.regression
def test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb26_invalid():
    case = Case(
        "test_bid_request_geo_targeting_for_countries_canada_states_ontario_rtb26_invalid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "fe088fc1-4cb4-548e-989b-6f8ff834e27d"
    vpc.ip_address = get_ip_not_for_geo(
        country="CA", region="Ontario", city="Toronto", postcode="M6H"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)
    # Validate the VAST Response

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(0)
