import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo


# This would test a placement that exists and check that is ok.
@pytest.mark.regression
def test_media_targeting_geo_for_dominican_republic():
    case = Case("test_media_targeting_geo_for_dominican_republic")

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="DO", city="Santo Domingo")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "DO"
    geo.cityName = "Santo Domingo"

    assert vast_result.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_media_targeting_geo_not_for_new_york():
    case = Case(
        "test_media_targeting_geo_not_for_new_york"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="US", city="New York")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Geo Targeting
    geo = case.assertionTargeting.geo
    geo.country = (
        "US"  # overwrite of the data file column `assert_targeting_geo_country`
    )
    geo.cityName = (
        "New York"  # overwrite of the data file column `assert_targeting_geo_cityName`
    )

    # Negative test case
    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_media_targeting_geo_for_new_york():
    case = Case(
        "test_media_targeting_geo_for_new_york"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(
        country="US", region="New York", city="New York", postcode="10065"
    )

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Overwrite of expected Geo Targeting
    geo = case.assertionTargeting.geo
    geo.country = (
        "US"  # overwrite of the data file column `assert_targeting_geo_country`
    )
    geo.cityName = (
        "New York"  # overwrite of the data file column `assert_targeting_geo_cityName`
    )
    geo.city = (
        "5128581"  # overwrite of the data file column `assert_targeting_geo_city`
    )
    geo.region = "NY"  # overwrite of the data file column `assert_targeting_geo_region`
    geo.regionName = "New York"  # overwrite of the data file column `assert_targeting_geo_regionName`
    geo.postalCode = (
        "10065"  # overwrite of the data file column `assert_targeting_geo_postalCode`
    )

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)
