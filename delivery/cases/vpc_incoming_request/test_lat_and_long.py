import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_geo_for_ip


# This would test that the Valid Latitude is present in delivery logs.
@pytest.mark.regression
def test_valid_latitude():
    case = Case("test_valid_latitude")  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818"
    )
    geo_data = get_geo_for_ip(vpc.ip_address)
    vpc.lat = geo_data["lat"]

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This will asssert that the value is passed
    vastResult.assertLogsDelivery([f"lat={geo_data['lat']}"])


# This would test that the Valid Longitude is present in delivery logs.
@pytest.mark.regression
def test_valid_longitude():
    case = Case("test_valid_longitude")  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818"
    )
    geo_data = get_geo_for_ip(vpc.ip_address)
    vpc.long = geo_data["lon"]

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery([f"longitude={geo_data['lon']}"])


# This would test that whether the Latitude is missing in delivery logs.
@pytest.mark.regression
def test_missing_latitude():
    case = Case("test_missing_latitude")  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818"
    )
    geo_data = get_geo_for_ip(vpc.ip_address)

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery([f"latitude={geo_data['lat']}"])


# This would test that whether Longitude is missing in delivery logs.
@pytest.mark.regression
def test_missing_longitude():
    case = Case("test_missing_longitude")  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818"
    )
    geo_data = get_geo_for_ip(vpc.ip_address)

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery([f"longitude={geo_data['lon']}"])


# This would test that the valid Latitude/longitude is present in delivery logs.
@pytest.mark.regression
def test_valid_latlng():
    case = Case("test_valid_latlng")  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818"
    )
    geo_data = get_geo_for_ip(vpc.ip_address)
    vpc.latlng = f"{geo_data['lat']}/{geo_data['lon']}"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery([f"latlng={geo_data['lat']}/{geo_data['lon']}"])


# This would test that whether the latitude/longitude is missing in delivery logs.
@pytest.mark.regression
def test_missing_latlng():
    case = Case("test_missing_latlng")  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="Oregon", city="Boardman", postcode="97818"
    )
    geo_data = get_geo_for_ip(vpc.ip_address)

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery(
        [f"latitude={geo_data['lat']}, longitude={geo_data['lon']}"]
    )
