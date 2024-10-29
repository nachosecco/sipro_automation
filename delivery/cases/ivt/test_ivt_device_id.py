import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.ivt import IVT


@pytest.mark.regression
def test_ivt_device_id_blocked():
    case = Case("test_ivt_device_id_blocked")

    vpc = case.vpc
    vpc.did = "472db8de-ec17-4722-80b7-cade19faf793"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.device_id == vpc.did

    # Assert Results
    assert ivt.response.is_passed == "false"
    assert ivt.response.checks.device_id.result == "MEETS_THRESHOLD"
    assert ivt.response.did_not_pass_category == "DEVICE_ID"

    vast_result.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_ivt_device_id_valid():
    case = Case("test_ivt_device_id_valid")

    vpc = case.vpc
    vpc.did = "1c3db86e-d237-5ca0-a179-df5fafe00bd7"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.device_id == vpc.did

    # Assert Results
    assert ivt.response.is_passed == "true"
    assert ivt.response.did_not_pass_category == ""

    vast_result.assertXML().assertAdsCount(1)


@pytest.mark.regression
def test_ivt_device_id_invalid():
    case = Case("test_ivt_device_id_invalid")

    vpc = case.vpc
    vpc.did = "not-a-valid-device-id"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # IVT shouldn't be called
    assert ivt.request.input_log_line_found is False

    assert ivt.filter_reason == "TARGETING_IVT_DEVICE_ID_INVALID"

    vast_result.assertXML().assertAdsCount(0)


@pytest.mark.regression
def test_ivt_device_id_valid_below_threshhold():
    case = Case("test_ivt_device_id_valid_below_threshhold")

    vpc = case.vpc
    vpc.did = "d76a47da-1f07-4abf-b5d0-244ebb60ef11"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.device_id == vpc.did

    # Assert Results
    assert ivt.response.is_passed == "true"
    assert ivt.response.did_not_pass_category == ""
    assert ivt.response.checks.device_id.result == "PASSED_UNDER_THRESHOLD"

    vast_result.assertXML().assertAdsCount(1)


@pytest.mark.regression
# When a privacy law is in place (in this case lmt=1)
# Delivery should send the real device id to IVT
# And When that id is in the block list
# Delivery should block the ad from being shown
# device-id used: 472db8de-ec17-4722-80b7-cade19faf793
# expected probability of 1.
# placement to be used: a ctv placement with ivt filtering enabled aligned to a media with ivt filtering enabled
# test expectations: No ad should be included in vast response
# test expectations: Delivery sends real device id information
def test_ivt_privacy_law_and_device_id():
    case = Case("test_ivt_privacy_law_and_device_id")

    vpc = case.vpc
    vpc.did = "472db8de-ec17-4722-80b7-cade19faf793"
    vpc.lmt = "1"

    vast_result = VastValidator().test(vpc)
    vast_result.assertCase(case)

    ivt = IVT(vast_result.deliveryLogs().logs)

    # Assert inputs
    assert ivt.request.device_id == vpc.did

    # Assert Results
    assert ivt.response.is_passed == "false"
    assert ivt.response.checks.device_id.result == "MEETS_THRESHOLD"
    assert ivt.response.did_not_pass_category == "DEVICE_ID"

    vast_result.assertXML().assertAdsCount(0)
