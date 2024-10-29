import pytest
from cases.rtb.ctv.test_bid_request_ctv import validate_rtb_ctv_common_properties
from core.case import Case
from core.vastValidator import VastValidator
from core.devices import (
    DEVICE_CTV_ROKU,
    DEVICE_SMARTPHONE_APPLE,
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


# This would test device targeting against connetedTV device Roku device vendor for version 2.6
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb26_valid():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb26_valid"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_CTV_ROKU.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # validate rtb version
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb26_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.6")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb26_valid",
    )

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb26(vpc.ip_address), True
    )


# This would test device targeting against connectedTV device Roku device vendor for version 2.5
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb25_valid():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb25_valid"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_CTV_ROKU.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # validate rtb version
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb25_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.5")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb25_valid",
    )

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb26(vpc.ip_address), True
    )


# This would test device targeting against connectedTV device Roku device vendor for version 2.4
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb24_valid():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb24_valid"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_CTV_ROKU.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # validate rtb version
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb24_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.4")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb24_valid",
    )

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb26(vpc.ip_address), True
    )


# This would test device targeting against connectedTV device Roku device vendor for version 2.3
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb23_valid():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb23_valid"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_CTV_ROKU.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # validate rtb version
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb23_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.3")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb23_valid",
    )

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb23(vpc.ip_address), True
    )


# This would test device targeting against connectedTV device Roku device vendor for version 2.2
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb22_valid():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb22_valid"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_CTV_ROKU.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)

    # validate rtb version
    bid_request_validator = vastResult.validate_rtb_bid_request()
    assert bid_request_validator.is_bidder_name_as_expected(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb22_valid"
    )
    assert bid_request_validator.is_rtb_version_as_expected("2.2")
    validate_rtb_ctv_common_properties(
        bid_request_validator,
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb22_valid",
    )

    # Validate device object in rtb bid request
    assert bid_request_validator.is_device_object_as_expected(
        get_expected_device_object_rtb22(vpc.ip_address), True
    )


# This would test device targeting against connectedTV device Roku device vendor for version 2.6 negative
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb26_negative():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb26_negative"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_SMARTPHONE_APPLE.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert not (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test device targeting against connectedTV device Roku device vendor for version 2.5 negative
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb25_negative():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb25_negative"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_SMARTPHONE_APPLE.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert not (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test device targeting against connectedTV device Roku device vendor for version 2.4 negative
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb24_negative():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb24_negative"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_SMARTPHONE_APPLE.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert not (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test device targeting against connectedTV device Roku device vendor for version 2.3 negative
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb23_negative():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb23_negative"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_SMARTPHONE_APPLE.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert not (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test device targeting against connectedTV device Roku device vendor for version 2.2 negative
@pytest.mark.regression
def test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb22_negative():
    case = Case(
        "test_media_device_targeting_ConnectedTV_bid_request_ctv_rtb22_negative"
    )  # This is the file to test this case

    vpc = case.vpc

    vpc.ua = DEVICE_SMARTPHONE_APPLE.ua
    vpc.did = "71299b6e-a1d8-4b20-bbfd-b271d9bbe5df"
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818", dma="810"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Device Targeting
    expectedDeviceTargeting = case.assertionTargeting.deviceTargeting

    expectedDeviceTargeting.type = DEVICE_CTV_ROKU.targeting_type
    expectedDeviceTargeting.os = DEVICE_CTV_ROKU.os.upper()

    assert not (
        vastResult.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expectedDeviceTargeting)
    )

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
