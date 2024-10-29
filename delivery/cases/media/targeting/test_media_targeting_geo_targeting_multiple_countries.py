import logging
import pytest
from core.case import Case
from core.targeting import GeoTargeting
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_multiple_countries_usa():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_multiple_countries_usa"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="US")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "US"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_multiple_countries_brazil():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_multiple_countries_brazil"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="BR")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_multiple_countries_mexico():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_multiple_countries_mexico"
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


# This would test a placement not returning media since it does not satisfy geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_multiple_countries_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_multiple_countries_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="AR")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    targeted_countries = ("MX", "US", "BR")
    for tc in targeted_countries:
        geo = GeoTargeting()
        geo.country = tc
        assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_multiple_countries_usa():
    case = Case(
        "test_media_targeting_geo_campaign_for_multiple_countries_usa"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="US")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "US"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_multiple_countries_brazil():
    case = Case(
        "test_media_targeting_geo_campaign_for_multiple_countries_brazil"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="BR")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_multiple_countries_mexico():
    case = Case(
        "test_media_targeting_geo_campaign_for_multiple_countries_mexico"
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


# This would test a placement not returning media since it does not satisfy geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_multiple_countries_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_multiple_countries_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="AR")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    targeted_countries = ("MX", "US", "BR")
    for tc in targeted_countries:
        geo = GeoTargeting()
        geo.country = tc
        assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_media_for_multiple_countries_usa():
    case = Case(
        "test_media_targeting_geo_media_for_multiple_countries_usa"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="US")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "US"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_media_for_multiple_countries_brazil():
    case = Case(
        "test_media_targeting_geo_media_for_multiple_countries_brazil"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="BR")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.country = "BR"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_media_for_multiple_countries_mexico():
    case = Case(
        "test_media_targeting_geo_media_for_multiple_countries_mexico"
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


# This would test a placement not returning media since it does not satisfy geo targeting for multiple countries(USA , Brazil ,Mexico) .
@pytest.mark.regression
def test_media_targeting_geo_media_for_multiple_countries_negative():
    case = Case(
        "test_media_targeting_geo_media_for_multiple_countries_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="AR")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    targeted_countries = ("MX", "US", "BR")
    for tc in targeted_countries:
        geo = GeoTargeting()
        geo.country = tc
        assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
