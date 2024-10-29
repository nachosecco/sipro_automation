import json
import logging
from core.case import Case
from core.logReader import LogReader, SavedLogReader
from core.rtbBidRequestValidator import RtbBidRequestValidator
from core.validator.rtb_auction_validator import RtbAuctionValidator
from core.vpc import VPC


class DisplayPlacementResultAssertor:
    def __init__(
        self,
        jsResponse,
        status: int,
        vpc: VPC,
        directoryPathVastResponse: str,
        vJsonPlayerResponse,
        tid,
    ):
        self.jsResponse = jsResponse
        self.status: int = status
        self.vpc = vpc
        self.directoryPathVastResponse = directoryPathVastResponse
        self.vJsonPlayerResponse = vJsonPlayerResponse
        self.logReader = LogReader(self.vpc)
        self.eventLogs = None
        self.dlp_response_content = self.parse_dlp_content(jsResponse)
        self.tid = tid
        self.logReader.set_tid(self.tid)

    # Runs all assertions in the case file and standard assertions
    def assertCase(self, case: Case):
        if len(case.logDelivery) == 0:
            logging.warning(
                "Expected delivery log assertion is empty in data file "
                + str(case.logDelivery)
            )
        else:
            logging.info("Expected Delivery logs " + str(case.logDelivery))

        self.assertLogsDelivery(case.logDelivery)

    def assertLogsDelivery(self, contains_to_test):
        if isinstance(contains_to_test, str):
            contains_to_test = contains_to_test.split(",")
        assert self.logReader.read_delivery(contains_to_test)

    def deliveryLogs(self):
        return SavedLogReader(
            "delivery",
            self.directoryPathVastResponse,
            self.logReader.find_logs_delivery(),
        )

    def validate_rtb_bid_request(self):
        return RtbBidRequestValidator(self.logReader.find_logs_delivery())

    def validate_rtb_auction(self):
        return RtbAuctionValidator(self.deliveryLogs().logs)

    @staticmethod
    def parse_dlp_content(response):
        content = str(response.content)
        content_proceed = content.split("proceed(", 1)[1]
        return json.loads(content_proceed.split("); }")[0])
