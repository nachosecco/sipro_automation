import logging
import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo

# This would test a placement that exists and check that is ok.


@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_usa_postalcode_alaska():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_usa_postalcode_alaska"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="US", postcode="99801")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Geo Targeting
    geo = case.assertionTargeting.geo
    geo.country = (
        "US"  # overwrite of the data file column `assert_targeting_geo_country`
    )
    geo.postalCode = (
        "99801"  # overwrite of the data file column `assert_targeting_geo_postalCode`
    )

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_usa_postalcode_alaska():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_usa_postalcode_alaska"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="US", postcode="99801")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Geo Targeting
    geo = case.assertionTargeting.geo
    geo.country = (
        "US"  # overwrite of the data file column `assert_targeting_geo_country`
    )
    geo.postalCode = (
        "99801"  # overwrite of the data file column `assert_targeting_geo_postalCode`
    )

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_media_targeting_geo_media_for_country_usa_postalcode_alaska():
    case = Case(
        "test_media_targeting_geo_media_for_country_usa_postalcode_alaska"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="US", postcode="99801")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Geo Targeting
    geo = case.assertionTargeting.geo
    geo.country = (
        "US"  # overwrite of the data file column `assert_targeting_geo_country`
    )
    geo.postalCode = (
        "99801"  # overwrite of the data file column `assert_targeting_geo_postalCode`
    )

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_usa_postalcode_alaska_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_usa_postalcode_alaska_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="US", postcode="99801")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Geo Targeting
    geo = case.assertionTargeting.geo
    geo.country = (
        "US"  # overwrite of the data file column `assert_targeting_geo_country`
    )
    geo.postalCode = (
        "99801"  # overwrite of the data file column `assert_targeting_geo_postalCode`
    )

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_usa_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_usa_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="US", postcode="99801")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Geo Targeting
    geo = case.assertionTargeting.geo
    geo.country = (
        "US"  # overwrite of the data file column `assert_targeting_geo_country`
    )
    geo.postalCode = (
        "99801"  # overwrite of the data file column `assert_targeting_geo_postalCode`
    )

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_media_targeting_geo_media_for_country_usa_negative():
    case = Case(
        "test_media_targeting_geo_media_for_country_usa_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="US", postcode="99801")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Geo Targeting
    geo = case.assertionTargeting.geo
    geo.country = (
        "US"  # overwrite of the data file column `assert_targeting_geo_country`
    )
    geo.postalCode = (
        "99801"  # overwrite of the data file column `assert_targeting_geo_postalCode`
    )

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
