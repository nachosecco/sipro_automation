import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo

# This would test a placement returning media that satisfies geo targeting for country mexico city guadalajara postalcode 44900 at IO level
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_mexico_city_guadalajara_postalcode_44900():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_mexico_city_guadalajara_postalcode_44900"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX", city="Guadalajara", postcode="44900")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo

    geo.country = "MX"
    geo.cityName = "Guadalajara"
    geo.postalCode = "44900"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for country mexico city guadalajara postalcode 44900 at campaign level
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_mexico_city_guadalajara_postalcode_44900():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_mexico_city_guadalajara_postalcode_44900"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX", city="Guadalajara", postcode="44900")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.cityName = "Guadalajara"
    geo.postalCode = "44900"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for country mexico city guadalajara postalcode 44900 at media level
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_mexico_city_guadalajara_postalcode_44900():
    case = Case(
        "test_media_targeting_geo_media_for_country_mexico_city_guadalajara_postalcode_44900"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX", city="Guadalajara", postcode="44900")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.cityName = "Guadalajara"
    geo.postalCode = "44900"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that does not satisfy geo targeting for country mexico city guadalajara postalcode 44900 at IO level
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_mexico_city_guadalajara_postalcode_44900_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_mexico_city_guadalajara_postalcode_44900_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(
        country="MX", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.cityName = "Guadalajara"
    geo.postalCode = "44900"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement returning media that does not satisfy geo targeting for country mexico city guadalajara postalcode 44900 at campaign level
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_mexico_city_guadalajara_postalcode_44900_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_mexico_city_guadalajara_postalcode_44900_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(
        country="MX", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "Mx"
    geo.cityName = "Guadalajara"
    geo.postalCode = "44900"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement returning media that does not satisfy geo targeting for country mexico city guadalajara postalcode 44900 at media level
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_mexico_city_guadalajara_postalcode_44900_negative():
    case = Case(
        "test_media_targeting_geo_media_for_country_mexico_city_guadalajara_postalcode_44900_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(
        country="MX", city="Guadalajara", postcode="44900"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.cityName = "Guadalajara"
    geo.postalCode = "44900"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
