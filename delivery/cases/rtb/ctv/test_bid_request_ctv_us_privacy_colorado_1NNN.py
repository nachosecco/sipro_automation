import pytest

from core.case import Case
from core.configuration import Configuration
from core.devices import DEVICE_CTV_ROKU
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_geo_for_ip


def validate_rtb_ctv_common_properties(bid_request_validator, case_name):
    assert bid_request_validator.is_placement_type_as_expected("mobile")
    assert bid_request_validator.is_required_properties_valid()
    assert bid_request_validator.is_video_object_valid()
    assert bid_request_validator.is_app_object_valid()

    assert bid_request_validator.is_app_object_as_expected(case_name)
    expected_regs = {"coppa": 0, "ext": {"gdpr": 0, "us_privacy": "1NNN"}}
    assert bid_request_validator.is_regs_object_as_expected(expected_regs)
    assert bid_request_validator.is_number_of_properties_as_expected(11)
    assert bid_request_validator.is_tmax_as_expected(Configuration().rtb_tmax)
    assert bid_request_validator.is_at_as_expected(2)
    assert bid_request_validator.is_allimps_as_expected(0)
    assert bid_request_validator.is_cur_as_expected(["USD"])


def get_expected_device_object_rtb22(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_device = {
        "ua": DEVICE_CTV_ROKU.ua,
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "USA",
            "region": "CO",
            "metro": "751",
            "city": "Denver",
            "zip": "80204",
            "type": 2,
        },
        "dnt": 0,
        "ip": ip_address,
        "devicetype": DEVICE_CTV_ROKU.rtb_type,
        "make": DEVICE_CTV_ROKU.make,
        "model": DEVICE_CTV_ROKU.model,
        "os": DEVICE_CTV_ROKU.os,
        "osv": DEVICE_CTV_ROKU.os_version,
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
            "region": "CO",
            "metro": "751",
            "city": "Denver",
            "zip": "80204",
            "type": 2,
        },
		"ext": {}
    }
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
def test_bid_request_ctv_us_privacy_colorado_1NNN_rtb22():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb22"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1NNN"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Colorado", city="Denver", postcode="80204", dma="751"
    )
    vpc.ua = DEVICE_CTV_ROKU.ua
    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb22"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb22"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb22(vpc.ip_address), True
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb22(vpc.ip_address)
    )
    assert bid_request_validator.is_ext_object_as_expected(
        get_expected_ext_object_rtb22(root_domain)
    )


def get_expected_device_object_rtb23(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_device = {
        "ua": DEVICE_CTV_ROKU.ua,
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "USA",
            "region": "CO",
            "metro": "751",
            "city": "Denver",
            "zip": "80204",
            "utcoffset": -420,
            "type": 2,
        },
        "dnt": 0,
        "lmt": 0,
        "ip": ip_address,
        "devicetype": DEVICE_CTV_ROKU.rtb_type,
        "make": DEVICE_CTV_ROKU.make,
        "model": DEVICE_CTV_ROKU.model,
        "os": DEVICE_CTV_ROKU.os,
        "osv": DEVICE_CTV_ROKU.os_version,
        "js": 0,
        "carrier": geo_data["carrier"],
        "connectiontype": geo_data["connection_type_code"],
        "ifa": "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df",
    }
    return expected_device


def get_expected_user_object_rtb23(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_user = {
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "USA",
            "region": "CO",
            "metro": "751",
            "city": "Denver",
            "zip": "80204",
            "utcoffset": -420,
            "type": 2,
        },
		"ext": {}
    }
    return expected_user


# Test RTB 2.3 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_us_privacy_colorado_1NNN_rtb23():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb23"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1NNN"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Colorado", city="Denver", postcode="80204", dma="751"
    )
    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb23"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb23"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb23(vpc.ip_address), True
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb23(vpc.ip_address)
    )
    assert bid_request_validator.is_ext_object_as_expected(
        get_expected_ext_object_rtb22(root_domain)
    )


def get_expected_device_object_rtb24(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_device = {
        "ua": DEVICE_CTV_ROKU.ua,
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "ipservice": 3,
            "country": "USA",
            "region": "CO",
            "metro": "751",
            "city": "Denver",
            "zip": "80204",
            "utcoffset": -420,
            "type": 2,
        },
        "dnt": 0,
        "lmt": 0,
        "ip": ip_address,
        "devicetype": DEVICE_CTV_ROKU.rtb_type,
        "make": DEVICE_CTV_ROKU.make,
        "model": DEVICE_CTV_ROKU.model,
        "os": DEVICE_CTV_ROKU.os,
        "osv": DEVICE_CTV_ROKU.os_version,
        "js": 0,
        "geofetch": 0,
        "carrier": geo_data["carrier"],
        "connectiontype": geo_data["connection_type_code"],
        "ifa": "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df",
    }
    return expected_device


def get_expected_user_object_rtb24(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_user = {
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "ipservice": 3,
            "country": "USA",
            "region": "CO",
            "metro": "751",
            "city": "Denver",
            "zip": "80204",
            "utcoffset": -420,
            "type": 2,
        },
		"ext": {}
    }
    return expected_user


# Test RTB 2.4 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_us_privacy_colorado_1NNN_rtb24():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb24"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1NNN"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Colorado", city="Denver", postcode="80204", dma="751"
    )
    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb24"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb24"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address), True
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )
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
def test_bid_request_ctv_us_privacy_colorado_1NNN_rtb25():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb25"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1NNN"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Colorado", city="Denver", postcode="80204", dma="751"
    )
    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb25"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb25"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address), True
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_source_object_as_expected(
        get_expected_source_object_rtb25(root_domain)
    )


# Test RTB 2.6 bid request for CTV placement
@pytest.mark.regression
def test_bid_request_ctv_us_privacy_colorado_1NNN_rtb26():
    root_domain = Configuration().root_domain
    case = Case(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb26"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.us_privacy = "1NNN"
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.did_type = "IDFA"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Colorado", city="Denver", postcode="80204", dma="751"
    )
    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # Validate the VAST Response
    vast_result.assertCase(case)

    # Validate the RTB Request
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb26"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ctv_us_privacy_colorado_1NNN_rtb26"
    )
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb24(vpc.ip_address), True
    )
    assert bid_request_validator.is_user_as_expected(
        get_expected_user_object_rtb24(vpc.ip_address)
    )
    assert bid_request_validator.is_source_object_as_expected(
        get_expected_source_object_rtb25(root_domain)
    )
