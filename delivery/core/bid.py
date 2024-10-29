from core.utils.stringUtils import subStringBetween


class Bid:
    def __init__(self, bid_str):
        self.price = subStringBetween(bid_str, "price=", ",")
        self.win_notice_url = subStringBetween(bid_str, "winNoticeUrl=", ",")
        self.loss_notice_url = subStringBetween(bid_str, "lossNoticeUrl=", ",")
        self.deal_id = subStringBetween(bid_str, "dealId=", ",")
        self.win_ad_markup = subStringBetween(bid_str, "winAdMarkup=", ",")
