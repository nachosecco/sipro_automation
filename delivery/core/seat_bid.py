from core.bid import Bid
from core.utils.stringUtils import subStringBetween


class SeatBid:
    def __init__(self, seat_bid_str):
        # Parse Seat Bid group
        self.group = subStringBetween(seat_bid_str, "group=", ",")
        # Parse Seat
        self.seat = subStringBetween(seat_bid_str, "seat=", ",")
        # Parse bids
        bids_str = subStringBetween(seat_bid_str, "bids=", ", seat=")
        bids = bids_str.split("Bid(")
        bids_len = len(bids)
        assert bids_len > 1, "There is no bid in Seat Bid"
        self.bids = []
        for i in range(1, bids_len):
            bid_str = bids[i].rstrip()
            bid = Bid(bid_str[:-2])
            self.bids.append(bid)
