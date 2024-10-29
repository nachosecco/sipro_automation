import pytest
from core.case import Case
from core.enums.gppSection import GPPSection

from core.Description import description
from core.utils.geoIpUtils import get_ip_for_geo
from core.vastValidator import VastValidator


@description(
    """Placement is aligned with 1 media that geo country targeting applied
    User has not allowed targeted advertising identified based on gpp string.
    TargetedAdvertisingOptOutNotice is 2 and TargetedAdvertisingOptOut is 1
    Ad should be blocked
    """
)
@pytest.mark.regression
def test_media_gpp_targeting_advertising_optedout_geo_targeting_applied():
    case = Case(
        "test_media_gpp_targeting_advertising_optedout_geo_targeting_applied"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABRg~BCEAAAA"  # when targeted advertising OptOut notice is two and OptOut is 1
    vpc.gpp_sid = GPPSection.VIRGINIA.id
    vpc.ip_address = get_ip_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that there is no ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


@description(
    """Placement is aligned with 1 media that geo country targeting applied
    User has allowed targeted advertising identified based on gpp string.
    TargetedAdvertisingOptOutNotice is 0 and TargetedAdvertisingOptOut is 1
    Ad should be served
    """
)
@pytest.mark.regression
def test_media_gpp_targeted_advertising_not_optedout_geo_targeting_applied():
    case = Case(
        "test_media_gpp_targeted_advertising_not_optedout_geo_targeting_applied"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = (
        "DBABRg~BAEAAAA"  # targeted advertising OptOut notice is zero and OptOut is one
    )
    vpc.gpp_sid = GPPSection.VIRGINIA.id
    vpc.ip_address = get_ip_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that there is no ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)
