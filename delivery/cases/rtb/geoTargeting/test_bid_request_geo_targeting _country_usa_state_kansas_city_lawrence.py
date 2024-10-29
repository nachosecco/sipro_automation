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
            "country": "USA",
            "region": "KS",
            "metro": "616",
            "city": "Lawrence",
            "zip": "66047",
            "type": 2,
        },
        "dnt": 0,
        "ip": ip_address,
        "os": "Other",
        "js": 0,
        "carrier": geo_data["carrier"],
        "connectiontype": geo_data["connection_type_code"],
        "ifa": "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df",
    }
    return expected_device


def get_expected_user_object_rtb22(ip_address):
    geo_data = get_geo_for_ip(ip_address)

    expected_user = {
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "USA",
            "region": "KS",
            "metro": "616",
            "city": "Lawrence",
            "zip": "66047",
            "type": 2,
        },
		"ext": {}
    }

    return expected_user


# Validating the geo targeting in RTB version 2.2 for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb22_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb22_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "US"
    geo.regionName = "Kansas"
    geo.cityName = "Lawrence"

    assert vast_result.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb22_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb22_valid",
    )
    # Validating the Device Object
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb22(vpc.ip_address)
    )
    # Validating the User Object
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb22(vpc.ip_address)
    )


# Validating the geo targeting in RTB version 2.2 not for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb22_negative():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb22_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_not_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This would assert there are no ads in the vast xml
    vast_result.assert_vast_xml().assert_ad_count(0)


def get_expected_device_object_rtb23(ip_address):
    expected_device = get_expected_device_object_rtb22(ip_address)
    expected_device["lmt"] = 0
    expected_device["geo"]["utcoffset"] = -360
    return expected_device


def get_expected_user_object_rtb23(ip_address):
    expected_device = get_expected_user_object_rtb22(ip_address)
    expected_device["geo"]["utcoffset"] = -360
    return expected_device


# Validating the geo targeting in RTB version 2.3 for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb23_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb23_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "US"
    geo.regionName = "Kansas"
    geo.cityName = "Lawrence"

    assert vast_result.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb23_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb23_valid",
    )
    # Validating the Device Object
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb23(vpc.ip_address)
    )
    # Validating the User Object
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb23(vpc.ip_address)
    )


# Validating the geo targeting in RTB version 2.3 not for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb23_negative():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb23_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_not_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This would assert there are no ads in the vast xml
    vast_result.assert_vast_xml().assert_ad_count(0)


def get_expected_device_object_rtb24(ip_address):
    expected_device = get_expected_device_object_rtb23(ip_address)
    expected_device["geo"]["ipservice"] = 3
    expected_device["geofetch"] = 0
    return expected_device


def get_expected_user_object_rtb24(ip_address):
    expected_user = get_expected_user_object_rtb22(ip_address)
    expected_user["geo"]["ipservice"] = 3
    expected_user["geo"]["utcoffset"] = -360
    return expected_user


# Validating the geo targeting in RTB version 2.4 for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb24_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb24_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "US"
    geo.regionName = "Kansas"
    geo.cityName = "Lawrence"

    assert vast_result.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb24_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb24_valid",
    )
    # Validating the Device Object
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    # Validating the User Object
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Validating the geo targeting in RTB version 2.4 not for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb24_negative():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb24_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_not_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(0)


# Validating the geo targeting in RTB version 2.5 for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb25_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb25_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "US"
    geo.regionName = "Kansas"
    geo.cityName = "Lawrence"

    assert vast_result.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb25_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb25_valid",
    )
    # Validating the Device Object
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    # Validating the User Object
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Validating the geo targeting in RTB version 2.5 not for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb25_negative():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb25_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_not_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This would assert there are no ads in the vast xml
    vast_result.assert_vast_xml().assert_ad_count(0)


# TValidating the geo targeting in RTB version 2.6 for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb26_valid():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb26_valid"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "US"
    geo.regionName = "Kansas"
    geo.cityName = "Lawrence"

    assert vast_result.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb26_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb26_valid",
    )
    # Validating the Device Object
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address)
    )
    # Validating the User Object
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )


# Validating the geo targeting in RTB version 2.6 not for country USA, State Kansas and City Lawrence
@pytest.mark.regression
def test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb26_negative():
    case = Case(
        "test_bid_request_geo_targeting_for_country_usa_kansas_lawrence_rtb26_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_not_for_geo(
        country="US", region="Kansas", city="Lawrence", postcode="66047"
    )

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This would assert there are no ads in the vast xml
    vast_result.assert_vast_xml().assert_ad_count(0)
