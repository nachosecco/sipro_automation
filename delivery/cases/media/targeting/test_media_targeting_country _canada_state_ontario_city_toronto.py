import logging
import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo


# This would test a placement returning media that satisfies geo targeting for Canada state ontario and city toronto
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_canada_state_ontario_city_toronto():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_canada_state_ontario_city_toronto"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="CA", region="Ontario", city="Toronto")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "CA"
    geo.regionName = "Ontario"
    geo.cityName = "Toronto"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for Canada state ontario and city toronto
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_canada_state_ontario_city_toronto():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_canada_state_ontario_city_toronto"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="CA", region="Ontario", city="Toronto")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "CA"
    geo.regionName = "Ontario"
    geo.cityName = "Toronto"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for Canada state ontario and city toronto
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_canada_state_ontario_city_toronto():
    case = Case(
        "test_media_targeting_geo_media_for_country_canada_state_ontario_city_toronto"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="CA", region="Ontario", city="Toronto")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "CA"
    geo.regionName = "Ontario"
    geo.cityName = "Toronto"
    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement not returning media since it does not satisfy geo targeting for Canada state Ontario and city Toronto
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_canada_state_ontario_city_toronto_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_canada_state_ontario_city_toronto_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="CA", region="Ontario", city="Toronto")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "CA"
    geo.regionName = "Ontario"
    geo.cityName = "Toronto"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement not returning media since it does not satisfy geo targeting for Canada state Ontario and city Toronto
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_canada_state_ontario_city_toronto_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_canada_state_ontario_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="CA", region="Ontario", city="Toronto")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "CA"
    geo.regionName = "Ontario"
    geo.cityName = "Toronto"
    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement not returning media since it does not satisfy geo targeting for Canada state Ontario and city Toronto
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_canada_state_ontario_city_toronto_negative():
    case = Case(
        "test_media_targeting_geo_media_for_country_canada_state_ontario_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="CA", region="Ontario", city="Toronto")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "CA"
    geo.regionName = "Ontario"
    geo.cityName = "Toronto"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
