from core.case import Case
from core.targeting import MediaSizeTargeting, MediaSize
from core.vastValidator import VastValidator
from core.enums.filterReason import FilterReason
import pytest


@pytest.mark.regression
def test_insertion_order_player_small_size_targeting():
    case = Case("test_insertion_order_player_small_size_targeting")

    vpc = case.vpc
    vpc.player_width = "200"
    vpc.player_height = "120"

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    vast_result.assertTargeting().media_size().expect(
        [MediaSizeTargeting(MediaSize.SMALL)]
    )

    vast_result.assertXML().assert_ad_count(1)


@pytest.mark.regression
def test_insertion_order_player_size_targeting_filtered():
    case = Case("test_insertion_order_player_size_targeting_filtered")

    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assertFilter(FilterReason.SIZES_RULE)
    vast_result.assertXML().assert_ad_count(0)


@pytest.mark.regression
def test_insertion_order_player_custom_size_targeting():
    case = Case("test_insertion_order_player_custom_size_targeting")

    vpc = case.vpc
    vpc.player_width = "400"
    vpc.player_height = "200"

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)
    vast_result.assertTargeting().media_size().expect(
        [MediaSizeTargeting(MediaSize.CUSTOM, "400200")]
    )

    vast_result.assertXML().assert_ad_count(1)


@pytest.mark.regression
def test_insertion_order_player_custom_size_targeting_filtered():
    case = Case("test_insertion_order_player_custom_size_targeting_filtered")

    vpc = case.vpc
    vpc.player_width = "200"
    vpc.player_height = "70"

    vast_result = VastValidator().test(vpc)

    vast_result.assertFilter(FilterReason.SIZES_RULE)
    vast_result.assertXML().assert_ad_count(0)
