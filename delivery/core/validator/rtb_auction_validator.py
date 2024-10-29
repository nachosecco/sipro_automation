import json
import logging

from core.bid_response import BidResponse
from core.dto.bidder import Bidder
from core.dto.pmp import PMP
from core.utils.stringUtils import subStringBetween
from core.utils.validationUtils import compare_values
from core.constants import ComparisonType as CT


class RtbAuctionValidator:
    def __init__(self, deliver_log):
        self.bidders = []
        self.loss_notice_urls = []
        self.__find_rtb_logs(deliver_log)

    def __find_rtb_logs(self, logs):
        for log in logs:
            if log.find("BID_request bidder bidder_id=") != -1:
                self.__parse_bidder_id(log)
                bidder = self.__find_or_create_bidder(self.bidder_id)
                self.__parse_bidder_name(log)
                bidder.bidder_name = self.bidder_name
                self.__parse_bid_request(log)
                bidder.bid_requests.append(self.bid_request)
            elif log.find("BID_request headers") != -1:
                self.__parse_bidder_id(log)
                bidder = self.__find_or_create_bidder(self.bidder_id)
                self.__parse_bid_request_headers(log)
                bidder.bid_request_rtb_versions.append(self.rtb_version)
                self.__parse_placement_type(log)
                bidder.bid_request_placement_types.append(self.placement_type)
            elif log.find("BID_response: Processing bid for bidder") != -1:
                bid_response = BidResponse(log)
                bidder = self.__find_or_create_bidder(bid_response.bidder_id)
                bidder.bid_responses.append(bid_response)
            elif log.find("Win notice - Url:") != -1:
                self.win_notice_url = subStringBetween(log, "Url: [", "]")
            elif log.find("Loss notice - Url:") != -1:
                self.loss_notice_urls.append(subStringBetween(log, "Url: [", "]"))
            elif (
                log.find("resolution is:") != -1
                and log.find("DefaultAuctionResolver") == -1
            ):
                self.__parse_auction_resolution(log)

    def __find_or_create_bidder(self, bidder_id):
        for bidder in self.bidders:
            if bidder.bidder_id == bidder_id:
                return bidder
        bidder = Bidder()
        bidder.bidder_id = bidder_id
        self.bidders.append(bidder)
        return bidder

    def __parse_bid_request(self, log_entry):
        bid_request_json = subStringBetween(log_entry, "json=", ", dealid=")
        self.bid_request = json.loads(bid_request_json)

    def __parse_bidder_id(self, log_entry):
        self.bidder_id = subStringBetween(log_entry, "bidder_id=", ",")

    def __parse_bidder_name(self, log_entry):
        self.bidder_name = subStringBetween(log_entry, "name=", ",")

    def __parse_bid_request_headers(self, log_entry):
        self.rtb_version = subStringBetween(
            log_entry, "x-openrtb-version:", ","
        ).strip()

    def __parse_placement_type(self, log_entry):
        self.placement_type = subStringBetween(log_entry, "placement_type=", ",")

    def __parse_auction_resolution(self, log):
        self.winning_bidder_name = subStringBetween(log, "winner=", "[")
        self.win_price = float(subStringBetween(log, "winPrice=", " "))
        self.applied_auction_type = subStringBetween(log, "appliedAuctionType=", "]")
        self.winning_deal_id = subStringBetween(log, "winningDealId=", " ")
        self.winning_seat_id = subStringBetween(log, "winningsSeatId=", ".")

    def is_win_notice_url_as_expected(self, url):
        return self.win_notice_url == url

    def is_winning_bidder_name_as_expected(self, expected_bidder_name):
        equal = self.winning_bidder_name == expected_bidder_name
        if not equal:
            logging.error(
                f"Expected winning_bidder_name is [{expected_bidder_name}] "
                f"the actual value is [{self.winning_bidder_name}]"
            )
        return equal

    def is_win_price_as_expected(self, expected_price):
        equals = self.win_price == expected_price
        if not equals:
            logging.error(
                f"expected win price is {expected_price} and the actual value is {self.win_price}"
            )
        return equals

    def is_applied_auction_type_as_expected(self, auction_type):
        return self.applied_auction_type == auction_type

    @staticmethod
    def __un_wrap_deal_id(deal_id):
        """In a case we could case we could a deal with a name 'winning_deal'
        in the environment could 'winning_deal_DA_003' we are going
         to improve to using the data of the environment with the class dataEnviroment.py"""
        if len(deal_id) > 7 and deal_id[-6:].startswith("DA_"):
            return deal_id[0 : len(deal_id) - 6]
        return deal_id

    def is_winning_deal_id_as_expected(self, expected_deal_id):
        actual_deal_id = self.__un_wrap_deal_id(self.winning_deal_id)
        equals = actual_deal_id == expected_deal_id
        if not equals:
            logging.error(
                f"Expected winning deal id is {expected_deal_id} and the actual value is {actual_deal_id}"
            )

        return equals

    def is_winning_seat_id_as_expected(self, seat_id):
        return self.winning_seat_id == seat_id

    def __is_pmp_object_as_expected(self, bid_request, expected_pmp: PMP):
        pmp = bid_request["imp"][0]["pmp"]
        compare_values(
            pmp["private_auction"],
            expected_pmp.private_auction,
            "private_auction",
            CT.Equality,
        )
        for expectedDeal in expected_pmp.deals:
            actual_deal = next(
                d
                for d in pmp["deals"]
                if self.__un_wrap_deal_id(d["id"]) == expectedDeal.id
            )

            assert actual_deal is not None, f"Deal {expectedDeal.id} not found"
            compare_values(
                self.__un_wrap_deal_id(actual_deal["id"]),
                expectedDeal.id,
                "deal id",
                CT.Equality,
            )
            compare_values(
                actual_deal["bidfloor"],
                expectedDeal.bid_floor,
                "bid_floor",
                CT.Equality,
            )
            compare_values(
                actual_deal["bidfloorcur"],
                expectedDeal.bid_floor_cur,
                "bid_floor_cur",
                CT.Equality,
            )

            if expectedDeal.wseat:
                assert actual_deal["wseat"]
                equals = sorted(actual_deal["wseat"]) == sorted(expectedDeal.wseat)
                if not equals:
                    logging.error(
                        f"Expected was [{sorted(expectedDeal.wseat)}], actual: [{sorted(actual_deal['wseat'])}]"
                    )

                assert (
                    equals
                ), f"Expected was ${sorted(expectedDeal.wseat)}, found: ${sorted(actual_deal['wseat'])}"

            compare_values(actual_deal["at"], expectedDeal.at, "at", CT.Equality)

    def are_pmp_objects_valid(self, expected_pmps: [PMP]):
        bidders = self.bidders
        length_bidders = len(bidders)
        length_expected = len(expected_pmps)
        equals_length = length_bidders == length_expected
        if not equals_length:
            logging.error(
                f"Bidders expected length is [{length_expected}] and the actual is [{length_bidders}]"
            )
        assert equals_length

        for bidder in self.bidders:
            # todo confirm how many bid request should be considered here, if more than one should we support that?
            bid_request = bidder.bid_requests[0]
            expected_pmp_for_bidder = None
            expected_bidders = []
            for expected_pmp in expected_pmps:
                expected_bidders.append(expected_pmp.bidder_name)
                if expected_pmp.bidder_name == bidder.bidder_name:
                    expected_pmp_for_bidder = expected_pmp
                    break
            if expected_pmp_for_bidder is None:
                logging.error(
                    f"The expected bidders are [{expected_bidders}] and is not found for the request "
                    f"the current bidder in the request is [{bidder.bidder_name}]"
                )
            assert (
                expected_pmp_for_bidder is not None
            ), f"PMP not found for bidder {bidder.bidder_name}"
            self.__is_pmp_object_as_expected(bid_request, expected_pmp_for_bidder)
