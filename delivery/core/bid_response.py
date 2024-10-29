from core.seat_bid import SeatBid
from core.utils.stringUtils import subStringBetween


class BidResponse:
    def __init__(self, log):
        self.__parse_bidder_id(log)
        self.__find_bid_response_string(log)
        self.__parse_id()
        self.__parse_bid_id()
        self.__parse_currency()
        self.seat_bids = []
        self.__parse_seat_bid()

    def __parse_bidder_id(self, log):
        self.bidder_id = subStringBetween(log, "id=", " ")

    def __find_bid_response_string(self, log):
        start_position = log.find("BidResponse(") + 12
        self.__bid_response_str = log[start_position:-2]

    # Parse the ID property in Bid Response which is the associated Bid Request ID according to Open RTB Spec.
    def __parse_id(self):
        self.id = subStringBetween(self.__bid_response_str, "id=", ",")

    def __parse_bid_id(self):
        self.bid_id = subStringBetween(self.__bid_response_str, "bidId=", ",")

    def __parse_currency(self):
        self.currency = subStringBetween(self.__bid_response_str, "currency=", ",")

    def __parse_seat_bid(self):
        seat_bids_str = subStringBetween(
            self.__bid_response_str, "seatBids=", ", bidId="
        )
        seat_bids = seat_bids_str.split("SeatBid(")
        seat_bids_len = len(seat_bids)
        assert seat_bids_len > 1
        for i in range(1, seat_bids_len):
            seat_bid_str = seat_bids[i].rstrip()
            seat_bid = SeatBid(seat_bid_str[:-2])
            self.seat_bids.append(seat_bid)
