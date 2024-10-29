import logging

from core.constants import ComparisonType as CT
from core.dto.bidder import Bidder
from core.utils.stringUtils import get_logs
from core.utils.validationUtils import compare_result, compare_result_without_quotes


class BidderAssertor:
    def __init__(self, logs):
        self.log = logs

    def __get_bidder_by_id(self, bidder_id):
        logging.info(f"bidder_id :##{bidder_id}##")
        for bidder in self.log:
            if bidder.find(f'id: "{bidder_id}"') > -1:
                return bidder
        return None

    def __find_and_validate_bidder(self, expectedBidder):
        if expectedBidder is not None:
            actualBidder = self.__get_bidder_by_id(expectedBidder.bidder_id)
            assert actualBidder is not None
            validate_bidder(actualBidder, expectedBidder)

    def assert_expected_bidders_in_logs(self, winningBidder: Bidder, losingBidders: []):
        self.__find_and_validate_bidder(winningBidder)
        for loserBidder in losingBidders:
            logging.info(loserBidder.__dict__)
            self.__find_and_validate_bidder(loserBidder)


def validate_bidder(log, expectedBidder):
    if log is not None:
        logging.debug("log" + log)
        compare_result('url: "', expectedBidder.bidder_url, log, CT.Startswith)
        compare_result_without_quotes("win: ", expectedBidder.win, log)
        compare_result('bidId: "', expectedBidder.bid_id, log)
        compare_result('bidCid: "', expectedBidder.bid_cid, log)
        compare_result('bidCrid: "', expectedBidder.bid_crid, log)
        compare_result_without_quotes("bidPrice: ", expectedBidder.bid_price, log)

        compare_result('bidAdDomains: "', expectedBidder.bid_ad_domains, log)
        compare_result('bidMediaGuid: "', expectedBidder.bid_media_guid, log)
        compare_result_without_quotes(
            "bidLossReasonCode: ",
            expectedBidder.bid_loss_reason_code,
            log,
        )
        compare_result(
            ' id: "', expectedBidder.bidder_id, log
        )  # space in id is required to skip matching other ids
        compare_result('bidDealId: "', expectedBidder.deal_id, log)


def parse_bidders_log(log):
    return get_logs(log, "bidders", "floor: ")
