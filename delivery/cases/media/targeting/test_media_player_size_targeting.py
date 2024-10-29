from core.case import Case
from core.targeting import MediaSize, MediaSizeTargeting
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason
import pytest


# Covers cases listed in ticket CP-2251


@pytest.mark.regression
def test_media_player_large_size_targeting():
    case = Case("test_media_player_large_size_targeting")

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertTargeting().media_size().expect(
        [MediaSizeTargeting(MediaSize.LARGE)]
    )

    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_media_player_medium_size_targeting():
    case = Case("test_media_player_medium_size_targeting")

    vpc = case.vpc
    vpc.player_width = "426"
    vpc.player_height = "240"
    vast_result = VastValidator().test(vpc)

    vast_result.assertTargeting().media_size().expect(
        [MediaSizeTargeting(MediaSize.MEDIUM)]
    )

    vast_result.assertCase(case)

    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_media_player_small_size_targeting():
    case = Case("test_media_player_small_size_targeting")

    vpc = case.vpc
    vpc.player_width = "120"
    vpc.player_height = "80"

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertTargeting().media_size().expect(
        [MediaSizeTargeting(MediaSize.SMALL)]
    )

    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_media_player_custom_size_targeting():
    case = Case("test_media_player_custom_size_targeting")

    vpc = case.vpc
    vpc.player_width = "500"
    vpc.player_height = "350"

    vast_result = VastValidator().test(vpc)

    vast_result.assertTargeting().media_size().expect(
        [MediaSizeTargeting(MediaSize.CUSTOM)]
    )

    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_media_player_custom_standard_size_targeting_filtered():
    case = Case("test_media_player_custom_standard_size_targeting_filtered")

    vpc = case.vpc
    vpc.player_width = "501"
    vpc.player_height = "350"

    vast_result = VastValidator().test(vpc)

    vast_result.assertFilter(FilterReason.SIZES_RULE)
    vast_result.assert_vast_xml().assert_ad_count(0)
