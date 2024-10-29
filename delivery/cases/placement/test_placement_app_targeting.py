import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason


@pytest.mark.regression
def test_placement_targeting_blocked_app_name():
    case = Case("test_placement_targeting_blocked_app_name")

    vpc = case.vpc
    vpc.app_name = "blocked_app_name"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_filter(FilterReason.APP_NAME_SUPPLY_SIDE)
    vast_result.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
def test_placement_targeting_blocked_app_name_filtered():
    case = Case("test_placement_targeting_blocked_app_name_filtered")

    vpc = case.vpc
    vpc.app_name = "other_than_blocked_app_name"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_not_empty()


@pytest.mark.regression
def test_placement_targeting_allowed_app_name():
    case = Case("test_placement_targeting_allowed_app_name")

    vpc = case.vpc
    vpc.app_name = "allowed_app_name"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_not_empty()


@pytest.mark.regression
def test_placement_targeting_allowed_app_name_filtered():
    case = Case("test_placement_targeting_allowed_app_name_filtered")

    vpc = case.vpc
    vpc.app_name = "invalid_allowed_app_name"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
def test_placement_targeting_blocked_app_id():
    case = Case("test_placement_targeting_blocked_app_id")
    vpc = case.vpc
    vpc.app_id = "blocked_app_id"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_filter(FilterReason.APP_BUNDLE_SUPPLY_SIDE)
    vast_result.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
def test_placement_targeting_blocked_app_id_filtered():
    case = Case("test_placement_targeting_blocked_app_id_filtered")
    vpc = case.vpc
    vpc.app_id = "other_than_blocked_app_id"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_not_empty()


@pytest.mark.regression
def test_placement_targeting_allowed_app_id():
    case = Case("test_placement_targeting_allowed_app_id")

    vpc = case.vpc
    vpc.app_id = "allowed_app_id"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_not_empty()


@pytest.mark.regression
def test_placement_targeting_allowed_app_id_filtered():
    case = Case("test_placement_targeting_allowed_app_id_filtered")

    vpc = case.vpc
    vpc.app_id = "invalid_allowed_app_id"
    vast_result = VastValidator().test(vpc)

    vast_result.assert_vast_xml().assert_ad_count(0)
