import logging
import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo


# This would test a placement returning media that satisfies geo targeting at IO level for Argentina state Cordoba City Villa del Rosario and postal code 5963
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000"
    )  # This is the file to test this case

    vpc = case.vpc
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
    geo.cityName = "Villa del Rosario"
    geo.postalCode = "5963"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting at campaign level for Argentina state Cordoba City Villa del Rosario and postal code 5963
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000"
    )  # This is the file to test this case

    vpc = case.vpc
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
    geo.cityName = "Villa del Rosario"
    geo.postalCode = "5963"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting at media level for Argentina state Cordoba City Villa del Rosario and postal code 5963
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000():
    case = Case(
        "test_media_targeting_geo_media_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000"
    )  # This is the file to test this case

    vpc = case.vpc
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
    geo.cityName = "Villa del Rosario"
    geo.postalCode = "5963"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement not returning media since it does not satisfy geo targeting at IO level for Argentina state Cordoba City Villa del Rosario and postal code 5963
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "AR"
    geo.regionName = "Cordoba"
    geo.cityName = "Villa del Rosario"
    geo.postalCode = "5963"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement not returning media since it does not satisfy geo targeting at campaign level for Argentina state Cordoba City Villa del Rosario and postal code 5963
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "AR"
    geo.regionName = "Cordoba"
    geo.cityName = "Villa del Rosario"
    geo.postalCode = "5963"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement not returning media since it does not satisfy geo targeting at media level for Argentina state Cordoba City Villa del Rosario and postal code 5963
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000_negative():
    case = Case(
        "test_media_targeting_geo_media_for_country_Argentina_state_Cordoba_city_VilladelRosario_postalcode_2000_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(
        country="AR", region="Cordoba", city="Villa del Rosario", postcode="5963"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "AR"
    geo.regionName = "Cordoba"
    geo.cityName = "Villa del Rosario"
    geo.postalCode = "5963"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
