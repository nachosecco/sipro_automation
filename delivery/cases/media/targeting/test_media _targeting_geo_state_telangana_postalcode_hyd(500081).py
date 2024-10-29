import logging
import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo, get_ip_not_for_geo


# This would test a placement returning media that satisfies geo targeting for Telangana and postal code 500081.
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_state_telangana_postalcode_hyd():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_state_telangana_postalcode_hyd"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(region="Telangana", postcode="500081")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.regionName = "Telangana"
    geo.postalCode = "500081"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for Telangana and postal code 500081.
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_state_telangana_postalcode_hyd():
    case = Case(
        "test_media_targeting_geo_campaign_for_state_telangana_postalcode_hyd"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(region="Telangana", postcode="500081")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.regionName = "Telangana"
    geo.postalCode = "500081"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement returning media that satisfies geo targeting for Telangana and postal code 500081.
@pytest.mark.regression
def test_media_targeting_geo_media_for_state_telangana_postalcode_hyd():
    case = Case(
        "test_media_targeting_geo_media_for_state_telangana_postalcode_hyd"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(region="Telangana", postcode="500081")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.regionName = "Telangana"
    geo.postalCode = "500081"

    assert vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo)

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)


# This would test a placement not returning media since it does not satisfy geo targeting for Telangana and postal code 500081.
@pytest.mark.regression
def test_media_targeting_geo_insertion_order_for_state_telangana_postalcode_hyd_negative():
    case = Case(
        "test_media_targeting_geo_insertion_order_for_state_telangana_postalcode_hyd_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(region="Telangana", postcode="500081")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.regionName = "Telangana"
    geo.postalCode = "500081"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement not returning media since it does not satisfy geo targeting for Telangana and postal code 500081.
@pytest.mark.regression
def test_media_targeting_geo_campaign_for_state_telangana_postalcode_hyd_negative():
    case = Case(
        "test_media_targeting_geo_campaign_for_state_telangana_postalcode_hyd_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(region="Telangana", postcode="500081")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.regionName = "Telangana"
    geo.postalCode = "500081"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


# This would test a placement not returning media since it does not satisfy geo targeting for Telangana and postal code 500081.
@pytest.mark.regression
def test_media_targeting_geo_media_for_state_telangana_postalcode_hyd_negative():
    case = Case(
        "test_media_targeting_geo_media_for_state_telangana_postalcode_hyd_negative"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_not_for_geo(region="Telangana", postcode="500081")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    geo = case.assertionTargeting.geo
    geo.regionName = "Telangana"
    geo.postalCode = "500081"

    assert not (vastResult.assertTargeting().geo().isExpectedGeoInTheLog(geo))

    # This would assert that is only one ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)
