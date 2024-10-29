class PMP:
    def __init__(self):
        self.private_auction = 0
        self.deals: [Deal] = None
        self.bidder_name = ""


class Deal:
    def __init__(self):
        self.id = ""
        self.bid_floor = ""
        self.bid_floor_cur = ""
        self.wseat = []
        self.at = ""
