import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.devices import DEVICE_SMARTPHONE_APPLE, DEVICE_CTV_ROKU, DEVICE_TABLET_LG


# This would test device targeting against a apple smartphone
@pytest.mark.regression
def test_media_device_targeting_type_smartphone_apple():
    case = Case("test_media_device_targeting_type_smartphone_apple")

    vpc = case.vpc

    vpc.ua = DEVICE_SMARTPHONE_APPLE.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # Overwrite of expected Device Targeting in data file
    expected_device_targeting = case.assertionTargeting.deviceTargeting

    expected_device_targeting.type = DEVICE_SMARTPHONE_APPLE.targeting_type
    expected_device_targeting.os = DEVICE_SMARTPHONE_APPLE.os.upper()
    expected_device_targeting.vendor = DEVICE_SMARTPHONE_APPLE.make
    expected_device_targeting.model = DEVICE_SMARTPHONE_APPLE.model

    assert (
        vast_result.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expected_device_targeting)
    )

    # This would assert that is only one ad in the vast xml
    vast_result.assert_vast_xml().assert_ad_count(1)


# This would test device targeting against a roku ctv
@pytest.mark.regression
def test_media_device_targeting_type_ctv_roku():
    case = Case("test_media_device_targeting_type_ctv_roku")

    vpc = case.vpc

    vpc.ua = DEVICE_CTV_ROKU.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # Overwrite of expected Device Targeting in data file
    expected_device_targeting = case.assertionTargeting.deviceTargeting

    expected_device_targeting.type = DEVICE_CTV_ROKU.targeting_type
    expected_device_targeting.vendor = DEVICE_CTV_ROKU.make

    assert (
        vast_result.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expected_device_targeting)
    )

    # This would assert that is only one ad in the vast xml
    vast_result.assertXML().assertAdsCount(1)


# This would test device targeting against a roku ctv
@pytest.mark.regression
def test_media_device_targeting_type_tablet_lg():
    case = Case("test_media_device_targeting_type_tablet_lg")

    vpc = case.vpc

    vpc.ua = DEVICE_TABLET_LG.ua

    # This would execute the framework
    vast_result = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vast_result.assertCase(case)

    # Overwrite of expected Device Targeting in data file
    expected_device_targeting = case.assertionTargeting.deviceTargeting

    expected_device_targeting.type = DEVICE_TABLET_LG.targeting_type
    expected_device_targeting.vendor = DEVICE_TABLET_LG.make

    assert (
        vast_result.assertTargeting()
        .device()
        .isExpectedDeviceTargetingInTheLog(expected_device_targeting)
    )

    # This would assert that is only one ad in the vast xml
    vast_result.assert_vast_xml().assert_ad_count(1)
