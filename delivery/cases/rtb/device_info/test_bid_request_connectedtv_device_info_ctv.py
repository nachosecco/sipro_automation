import pytest

from cases.rtb.ctv.test_bid_request_ctv import validate_rtb_ctv_common_properties
from core.case import Case
from core.vastValidator import VastValidator
from core.devices import (
    DEVICE_CTV_ROKU,
)
from core.utils.geoIpUtils import get_ip_for_geo, get_geo_for_ip


def get_expected_device_object_rtb22(ip_address):
    geo_data = get_geo_for_ip(ip_address)
    expected_device = {
        "ua": DEVICE_CTV_ROKU.ua,
        "geo": {
            "lat": float(geo_data["lat"]),
            "lon": float(geo_data["lon"]),
            "country": "USA",
            "region": "OR",
            "metro": "810",
            "city": "Boardman",
            "zip": "97818",
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


def get_expected_device_object_rtb23(ip_address):
    expected_device = get_expected_device_object_rtb22(ip_address)
    expected_device["geo"]["utcoffset"] = -480
    expected_device["lmt"] = 0
    return expected_device


def get_expected_device_object_rtb24(ip_address):
    expected_device = get_expected_device_object_rtb22(ip_address)
    expected_device["geo"]["ipservice"] = 3
    expected_device["geofetch"] = 0
    return expected_device


def get_expected_device_object_rtb26(ip_address):
    expected_device = get_expected_device_object_rtb24(ip_address)
    expected_device["geo"]["utcoffset"] = -480
    expected_device["lmt"] = 0
    return expected_device


# This would test device info against connetedTV device Roku device vendor for version 2.6
@pytest.mark.regression
def test_bid_request_ConnectedTV_device_info_rtb26():
    case = Case(
        "test_bid_request_ConnectedTV_device_info_rtb26"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"

    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # validate rtb version
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ConnectedTV_device_info_rtb26"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb26(vpc.ip_address), True
    )


# This would test device info against connectedTV device Roku device vendor for version 2.5
@pytest.mark.regression
def test_bid_request_ConnectedTV_device_info_rtb25():
    case = Case(
        "test_bid_request_ConnectedTV_device_info_rtb25"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"

    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # validate rtb version
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ConnectedTV_device_info_rtb25"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb26(vpc.ip_address), True
    )


# This would test device info against connectedTV device Roku device vendor for version 2.4
@pytest.mark.regression
def test_bid_request_ConnectedTV_device_info_rtb24():
    case = Case(
        "test_bid_request_ConnectedTV_device_info_rtb24"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"

    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # validate rtb version
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ConnectedTV_device_info_rtb24"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb26(vpc.ip_address), True
    )


# This would test device info against connectedTV device Roku device vendor for version 2.3
@pytest.mark.regression
def test_bid_request_ConnectedTV_device_info_rtb23():
    case = Case(
        "test_bid_request_ConnectedTV_device_info_rtb23"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)

    # validate rtb version
    bid_request_validator = vast_result.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ConnectedTV_device_info_rtb23"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator, "test_bid_request_ConnectedTV_device_info_rtb23"
    )

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb23(vpc.ip_address), True
    )


# This would test device info against connectedTV device Roku device vendor for version 2.2
@pytest.mark.regression
def test_bid_request_ConnectedTV_device_info_rtb22():
    case = Case("test_bid_request_ConnectedTV_device_info_rtb22")
    # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"

    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that is only one ad in the vast xml
    # vastResult.assertXML().assertAdsCount(1)

    # validate rtb versions
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_bid_request_ConnectedTV_device_info_rtb22"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb22(vpc.ip_address), True
    )
