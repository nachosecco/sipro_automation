import pytest
from core.case import Case
from core.contentInfo import (
    content_catagory_IAB_1,
    ProductionQuality_3,
    qagmediarating_1,
    livestream_1,
)
from core.vastValidator import VastValidator
from core.dto.event import Event
from core.constants import UNKNOWN
from core.dto.event import EventType


# This would test whether event sent for an demand opportunity are expected.
@pytest.mark.regression
def test_delivery_automation_demand_opportunity_event():
    case = Case("test_delivery_automation_demand_opportunity_event")
    vpc = case.vpc
    vpc.geo_co = "US"
    vpc.geo_dma = "New York"
    vpc.geo_sub = "sub"
    vpc.geo_subname = "subname"
    vpc.geo_code = "NY"
    vpc.geo_conn_type = "conn_type"
    vpc.geo_lat = "23423.22"
    vpc.geo_long = "23423.23"
    vpc.geo_isp_name = "isp_name"
    vpc.app_id = "app_id"
    vpc.app_name = "app_name"
    vpc.did = "03055002-06e6-5737-94aa-3e9ddda81953"

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    event = case.event
    event.event_type = EventType.demandopportunity
    event.user_agent = "python-requests"
    event.placement_size = "640x480"
    event.device_type = UNKNOWN
    event.media_type = "VAST"
    event.os = "OTHER"
    event.ipAddressOverride = ""

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_delivery_automation_demand_opportunity_event_filtered():
    case = Case("test_delivery_automation_demand_opportunity_event_filtered")
    vpc = case.vpc
    vpc.app_id = "app_id"
    vpc.app_name = "atlantic icebergs images"
    vpc.did = "03055002-06e6-5737-94aa-3e9ddda81953"

    vast_result = VastValidator().test(vpc)

    vast_result.assertCase(case)

    event = Event()
    event.event_type = EventType.demandopportunity
    event.user_agent = "python-requests"
    event.placement_size = "640x480"
    event.filter_reason = "TARGETING_COUNTRY"
    event.ipAddressOverride = ""

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(0)


@pytest.mark.regression
def test_delivery_autumation_demand_opportunity_event_content_info():
    case = Case("test_delivery_autumation_demand_opportunity_event_content_info")
    vpc = case.vpc
    vpc.content_episode = "10"
    vpc.content_title = "Flash"
    vpc.content_series = "10"
    vpc.content_genre = "comedy"
    vpc.content_cat = "IAB_1"
    vpc.content_prodq = "3"
    vpc.content_qagmediarating = "1"
    vpc.content_livestream = "1"
    vpc.content_len = "30"
    vpc.content_language = "ENG"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.demandopportunity
    event.ipAddressOverride = ""
    event.episode = vpc.content_episode
    event.title = vpc.content_title
    event.series = vpc.content_series
    event.genre = vpc.content_genre
    event.categories = content_catagory_IAB_1
    event.productionQuality = ProductionQuality_3
    event.mediaRating = qagmediarating_1
    event.liveStream = livestream_1
    event.length = vpc.content_len
    event.language = vpc.content_language

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@pytest.mark.regression
def test_delivery_autumation_demand_opportunity_event_content_info_negative():
    case = Case(
        "test_delivery_autumation_demand_opportunity_event_content_info_negative"
    )
    vpc = case.vpc
    vpc.content_episode = "10"
    vpc.content_title = "Flash"
    vpc.content_series = "10"
    vpc.content_genre = "comedy"
    vpc.content_cat = "IAB1-22"
    vpc.content_prodq = "333"
    vpc.content_qagmediarating = "7"
    vpc.content_livestream = "111"
    vpc.content_len = "30"
    vpc.content_language = "ENG"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.demandopportunity
    event.ipAddressOverride = ""
    event.episode = vpc.content_episode
    event.title = vpc.content_title
    event.series = vpc.content_series
    event.genre = vpc.content_genre
    event.categories = ""
    event.productionQuality = ""
    event.mediaRating = ""
    event.liveStream = ""
    event.length = vpc.content_len
    event.language = vpc.content_language

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)
