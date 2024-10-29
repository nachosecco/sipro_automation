import pytest
from core.case import Case
from core.enums.gppSection import GPPSection

from core.Description import description
from core.utils.geoIpUtils import get_ip_for_geo
from core.vastValidator import VastValidator


@description(
    """Placement is aligned with 1 media. Placement has app name targeting applied
    User has not allowed targeted advertising identified based on gpp string.
    TargetedAdvertisingOptOutNotice is 1 and TargetedAdvertisingOptOut is 0
    Ad should be blocked
    """
)
@pytest.mark.regression
def test_placement_gpp_targeted_advertising_optedout_appName_targeting_applied():
    case = Case(
        "test_placement_gpp_targeted_advertising_optedout_appName_targeting_applied"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABRg~BBEAAAA"  # when targeted advertising OptOut notice is one and OptOut is one
    vpc.gpp_sid = GPPSection.VIRGINIA.id
    vpc.ip_address = get_ip_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that there is no ad in the vast xml
    vastResult.assertXML().assertAdsCount(0)


@description(
    """Placement is aligned with 1 media. Placement has app name targeting applied
    User has allowed targeted advertising identified based on gpp string.
    TargetedAdvertisingOptOutNotice is 1 and TargetedAdvertisingOptOut is 2
    Ad should be served
    """
)
@pytest.mark.regression
def test_placement_gpp_targeted_advertising_not_optedout_appName_targeting_applied():
    case = Case(
        "test_placement_gpp_targeted_advertising_not_optedout_appName_targeting_applied"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.gpp = "DBABRg~BBIAAAA"  # when targeted advertising OptOut notice is one and OptOut is two
    vpc.gpp_sid = GPPSection.VIRGINIA.id
    vpc.ip_address = get_ip_for_geo(country="MX")

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This would assert that there is no ad in the vast xml
    vastResult.assertXML().assertAdsCount(1)
