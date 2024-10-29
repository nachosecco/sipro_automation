import logging
import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo


# This would test a placement returning media that satisfies geo targeting for country mexico state jalisco at IO level
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_mexico_state_jalisco():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_mexico_state_jalisco"
    )

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX", region="Jalisco")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo

    geo.country = "MX"
    geo.regionName = "Jalisco"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that
# satisfies geo targeting for country mexico state jalisco at campaign level
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_mexico_state_jalisco():
    case = Case("test_media_targeting_geo_campaign_for_country_mexico_state_jalisco")

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX", region="Jalisco")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.regionName = "Jalisco"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for country mexico state jalisco at media level
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_mexico_state_jalisco():
    case = Case(
        "test_media_targeting_geo_media_for_country_mexico_state_jalisco"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX", region="Jalisco")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.regionName = "Jalisco"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that does not satisfy geo targeting for country mexico state jalisco at IO level
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_mexico_state_jalisco_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_mexico_state_jalisco_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="MX", region="Jalisco")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.regionName = "Jalisco"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement returning media that does not satisfy geo targeting for country mexico state jalisco at campaign level
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_mexico_state_jalisco_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_mexico_state_jalisco_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="MX", region="Jalisco")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.regionName = "Jalisco"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement returning media that does not satisfy geo targeting for country mexico state jalisco at media level
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_mexico_state_jalisco_negative():
    case = Case(
        "test_media_targeting_geo_media_for_country_mexico_state_jalisco_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="MX", region="Jalisco")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"
    geo.regionName = "Jalisco"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)