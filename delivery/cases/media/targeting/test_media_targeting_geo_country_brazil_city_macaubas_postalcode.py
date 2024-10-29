import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo


# This would test a placement that exists and check that is ok.


@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_brazil_city_macaubas_postalcode_46500():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_brazil_city_macaubas_postalcode_46500"
    )

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="BR", city="Macaubas", postcode="46500")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"
    geo.cityName = "Macaubas"
    geo.postalCode = "46500"

    assert vast_result.assertTargeting().geo().is_expected_geo(geo)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_brazil_city_macaubas_postalcode_46500():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_brazil_city_macaubas_postalcode_46500"
    )

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="BR", city="Macaubas", postcode="46500")

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"
    geo.cityName = "Macaubas"
    geo.postalCode = "46500"

    assert vast_result.assertTargeting().geo().is_expected_geo(geo)

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_media_targeting_geo_media_for_country_brazil_city_macaubas_postalcode_46500():
    case = Case(
        "test_media_targeting_geo_media_for_country_brazil_city_macaubas_postalcode_46500"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="BR", city="Macaubas", postcode="46500")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"
    geo.cityName = "Macaubas"
    geo.postalCode = "46500"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_country_brazil_city_macaubas_postalcode_46500_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_country_brazil_city_macaubas_postalcode_46500_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="BR", city="Macaubas", postcode="46500")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"
    geo.cityName = (
        "Macaubas"  # overwrite of the data file column `assert_targeting_geo_cityName`
    )
    geo.postalCode = (
        "46500"  # overwrite of the data file column `assert_targeting_geo_postalCode`
    )

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_media_targeting_geo_campaign_for_country_brazil_city_macaubas_postalcode_46500_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_country_brazil_city_macaubas_postalcode_46500_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="BR", city="Macaubas", postcode="46500")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"
    geo.cityName = "Macaubas"
    geo.postalCode = "46500"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_media_targeting_geo_media_for_country_brazil_city_macaubas_postalcode_46500_negative():
    case = Case(
        "test_media_targeting_geo_media_for_country_brazil_city_macaubas_postalcode_46500_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(country="BR", city="Macaubas", postcode="46500")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"
    geo.cityName = "Macaubas"
    geo.postalCode = "46500"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
