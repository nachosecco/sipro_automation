import logging

from core.dto.event import Event
from core.utils.validationUtils import compare_result
from core.vpc import VPC
from core.utils.stringUtils import get_logs


class EventAppLogsAssertor:
    def __init__(self, savedLogs, vpc: VPC):
        self.event = None
        self.savedLogs = savedLogs
        self.logFound = False
        self.log = ""
        self.vpc = vpc

    def assert_expected_event_in_the_log(self, event: Event, message: str):
        self.event = event
        self.log = find_log_entry(self.savedLogs, message).strip()
        self.logFound = len(self.log) != 0
        self.validate_event()
        self.validate_rtb_meta()

    def validate_event(self):
        logging.info(
            f"Asserting that the expected event values are : ${self.event.__dict__}"
        )

        if not self.logFound:
            logging.error(
                "The log message related to event targeting was not found in the logs"
            )
            assert False
        # add more event values to validate here

    def validate_rtb_meta(self):
        event = self.event
        rtb_meta = self.__get_rtb_meta()
        compare_result('adomain: "', event.winnerBidder.bid_ad_domains, rtb_meta)
        compare_result('cid: "', event.winnerBidder.bid_cid, rtb_meta)
        compare_result('crid: "', event.winnerBidder.bid_crid, rtb_meta)
        compare_result('dealid: "', event.winnerBidder.deal_id, rtb_meta)
        compare_result('bidderGuid: "', event.winnerBidder.bidder_id, rtb_meta)
        compare_result('placementGuid: "', event.placement_guid, rtb_meta)
        compare_result('dealGuid: "', event.winnerBidder.deal_guid, rtb_meta)
        compare_result('seatId: "', event.winnerBidder.seat_id, rtb_meta)

    def __get_rtb_meta(self):
        rtb_metas = get_logs(self.log, "rtbMetas: [", "], eventType")
        if rtb_metas is None or len(rtb_metas) == 0:
            logging.error("RTB Meta record not found")
            assert False, "RTB Meta record not found"
        return rtb_metas[0]


def find_log_entry(logs, message: str):
    for log in logs:
        if log.find(message) != -1:
            return log
    return ""
