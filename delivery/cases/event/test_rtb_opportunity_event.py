import pytest

from core.Description import description
from core.case import Case
from core.contentInfo import (
    content_catagory_IAB_1,
    ProductionQuality_3,
    qagmediarating_1,
    livestream_1,
)
from core.dto.bidder import Bidder
from core.vastValidator import VastValidator
from core.constants import UNKNOWN
from core.constants import NUMBER_PLACEHOLDER, FAKE_BIDDER_URL
from core.dto.event import EventType


@description(
    "This would test whether events sent for a rtb opportunity have the expected fields."
)
@pytest.mark.regression
def test_rtb_opportunity_event():
    case = Case("test_rtb_opportunity_event")
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

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.wcpm = "10.0"
    event.cpm = "10.0"
    event.floor = "0.01"
    event.placement_size = "640x480"
    event.placement_type = "MOBILE"
    event.device_type = UNKNOWN
    event.vpaid_type = "VAST"
    event.device_os = "OTHER"
    event.result = "BID"

    winner_bidder = Bidder()
    winner_bidder.response_time = NUMBER_PLACEHOLDER  # greater than
    winner_bidder.bid_id = "vast_seat1-bid1"
    winner_bidder.bidder_url = FAKE_BIDDER_URL
    winner_bidder.bid_price = "10.0"
    winner_bidder.deal_id = "dealAuto1"
    winner_bidder.bid_ad_domains = "https://www.smaato.com"
    winner_bidder.bid_loss_reason_code = "BID_WON"
    winner_bidder.win = "true"
    winner_bidder.bid_cid = "24451"
    winner_bidder.bid_crid = "16969421"
    event.winner_id = winner_bidder.bidder_id

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    vast_result.assert_vast_xml().assert_ad_count(1)

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)


@description(
    "This would test whether the event sent for a rtb opportunity has sessionId flag set to true"
)
@pytest.mark.regression
def test_rtb_opportunity_event_for_sessionid_flag_true():
    case = Case("test_rtb_opportunity_event_for_sessionid_flag_true")
    vpc = case.vpc
    vpc.player_height = "480"
    vpc.player_width = "640"

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.wcpm = "0.02"
    event.cpm = "10.051027"
    event.floor = "0.01"
    event.placement_size = "640x480"
    event.placement_type = "MOBILE"
    event.device_type = UNKNOWN
    event.vpaid_type = "VAST"
    event.device_os = "OTHER"
    event.result = "BID"
    event.is_using_user_tracker_id_session_UUID = "true"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    vast_result.assert_event().assert_expected_event_in_the_log(event)
    vast_result.assert_vast_xml().assert_ad_count(1)


@description(
    "This would test whether event sent for a rtb opportunity has the correct content info data"
)
@pytest.mark.regression
def test_delivery_autumation_RTB_event_content_info():
    case = Case("test_delivery_autumation_RTB_event_content_info")
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

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.wcpm = "0.02"
    event.cpm = "10.051027"
    event.floor = "0.01"
    event.placement_size = "640x480"
    event.placement_type = "MOBILE"
    event.device_type = UNKNOWN
    event.vpaid_type = "VAST"
    event.device_os = "OTHER"
    event.result = "BID"
    event.is_using_user_tracker_id_session_UUID = "true"
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

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)


@description(
    "This would test negatively whether event sent for a rtb opportunity has the correct content info"
)
@pytest.mark.regression
def test_delivery_autumation_RTB_event_content_info_negative():
    case = Case("test_delivery_autumation_RTB_event_content_info_negative")
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

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.ipAddressOverride = ""
    event.wcpm = "0.02"
    event.cpm = "10.051027"
    event.floor = "0.01"
    event.placement_size = "640x480"
    event.placement_type = "MOBILE"
    event.device_type = UNKNOWN
    event.vpaid_type = "VAST"
    event.device_os = "OTHER"
    event.result = "BID"
    event.is_using_user_tracker_id_session_UUID = "true"
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

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)


@description(
    "This would test whether event sent for a rtb opportunity has the correct fields"
    " when using bidder of 2.6 and impExp field"
)
@pytest.mark.regression
def test_delivery_autumation_RTB_event_impexp_2_6():
    case = Case("test_delivery_autumation_RTB_event_impexp_2_6")
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.ipAddressOverride = ""
    event.impExp = "7200"
    event.wcpm = "0.11"

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@description(
    "This would test whether the event sent for a rtb opportunity is correct when using bidder of 2.5 and impExp field"
)
@pytest.mark.regression
def test_delivery_autumation_RTB_event_impexp_2_5():
    case = Case("test_delivery_autumation_RTB_event_impexp_2_5")
    vpc = case.vpc

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.ipAddressOverride = ""
    event.impExp = "7200"
    event.wcpm = "0.11"

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@description(
    "This would test whether the event sent for a rtb opportunity when using bidder of 2.4 and impExp field"
)
@pytest.mark.regression
def test_delivery_autumation_RTB_event_impexp_2_4():
    case = Case("test_delivery_autumation_RTB_event_impexp_2_4")
    vpc = case.vpc
    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.ipAddressOverride = ""
    event.impExp = "7200"
    event.wcpm = "0.11"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@description(
    """This would test instream(vast)
      whether the event sent for a rtb opportunity is correct when using bidder of 2.4 and impExp field"""
)
@pytest.mark.regression
def test_delivery_autumation_vast_RTB_event_impexp_2_4():
    case = Case("test_delivery_autumation_vast_RTB_event_impexp_2_4")
    vpc = case.vpc
    vpc.page_url = "siprocal.com"

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.ipAddressOverride = ""
    event.impExp = "300"
    event.wcpm = "0.02"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@description(
    """This would test instream(vast)
     whether event sent for a rtb opportunity is correct when using bidder of 2.5 and impExp field"""
)
@pytest.mark.regression
def test_delivery_autumation_vast_RTB_event_impexp_2_5():
    case = Case("test_delivery_autumation_vast_RTB_event_impexp_2_5")
    vpc = case.vpc
    vpc.page_url = "siprocal.com"

    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.ipAddressOverride = ""
    event.impExp = "300"
    event.wcpm = "0.02"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@description(
    """This would test instream(vast)
     whether the event sent for a rtb opportunity is correct when using bidder of 2.6 and impExp field"""
)
@pytest.mark.regression
def test_delivery_autumation_vast_RTB_event_impexp_2_6():
    case = Case("test_delivery_autumation_vast_RTB_event_impexp_2_6")
    vpc = case.vpc
    vpc.page_url = "siprocal.com"
    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.ipAddressOverride = ""
    event.impExp = "300"
    event.wcpm = "0.02"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)

    vast_result.assert_vast_xml().assert_ad_count(1)


@description("This would test whether event sent for a rtb bid contains a win")
@pytest.mark.regression
def test_rtb_event_bid_won():
    case = Case("test_rtb_event_bid_won")
    vpc = case.vpc
    event = case.event
    event.event_type = EventType.RTB_EVENT
    event.bid_win = "true"
    event.loss_reason_code = "BID_WON"
    event.impId = "1"

    vast_result = VastValidator().test(vpc)

    vast_result.assert_case(case)

    # This will execute the all assertions to validate events
    vast_result.assert_event().assert_expected_event_in_the_log(event)
