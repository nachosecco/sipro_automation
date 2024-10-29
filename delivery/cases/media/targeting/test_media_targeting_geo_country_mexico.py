import logging
import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo


# This would test a placement returning media that satisfies geo targeting for country mexico at IO level.
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_mexico():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_mexico"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for country mexico at Campaign level.
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_mexico():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_mexico"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for country mexico at media level.
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_mexico():
    case = Case(
        "test_media_targeting_geo_media_for_country_mexico"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning no media that do not satisfy geo targeting for country mexico at IO level.
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_mexico_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_mexico_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that there is no ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement returning no media that do not satisfy geo targeting for country mexico at campaign level.
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_mexico_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_mexico_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that there is no ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement returning no media that do not satisfy geo targeting for country mexico at media level.
@pytest.mark.regression
def test_media_targeting_geo_media_for_country_mexico_negative():
    case = Case(
        "test_media_targeting_geo_media_for_country_mexico_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "MX"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that there is no ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
