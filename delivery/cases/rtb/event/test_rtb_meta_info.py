import copy

import pytest
from core.case import Case
from core.dto.bidder import Bidder
from core.vastValidator import VastValidator
from core.configuration import Configuration


# This would test whether event sent for a rtb opportunity has right meta info as expected.
@pytest.mark.regression
def test_rtb_meta_info_event():
    case = Case("test_rtb_meta_info_event")
    configOverride: Configuration = copy.deepcopy(Configuration())
    configOverride.open_search_time_to_wait_to_read_event_log = 10
    configOverride.open_search_time_to_wait_to_read_event_tid = 5
    configOverride.open_search_time_to_wait_to_read_event_log_2ndTime = 5
    configOverride.read_event_logs = True

    vpc = case.vpc
    vpc.app_id = "app_id"
    vpc.app_name = "app_name"

    event = case.event
    winner_bidder = Bidder()

    winner_bidder.deal_id = "dealAutoRTBMetaInfo"
    winner_bidder.bid_ad_domains = "https://www.smaato.com"
    winner_bidder.seat_id = "Seat3"

    vast_result = VastValidator().test(vpc, 200, configOverride)

    vast_result.assertCase(case)

    vast_result.assertXML().assert_ad_count(1)
