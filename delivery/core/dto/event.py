from enum import Enum

from core.dto.bidder import Bidder


class Event:
    """Class that is used to carry information of the event that we are going to assert"""

    def __init__(self):
        self.event_type: EventType = None
        self.company_guid = ""
        self.publisher_guid = ""
        self.advertiser_guid = ""
        self.site_guid = ""
        self.placement_guid = ""
        self.user_agent = ""
        self.user_tracker_id = ""
        self.placement_size = ""
        self.placement_position = 0
        self.placement_type = 0
        self.partner_guid = ""
        self.floor = ""
        self.cpm = ""
        self.placement_size_type = 0
        self.beacon_event_type = ""
        self.ipAddressOverride = ""
        self.schain = ""
        self.ipAddress = ""
        self.blocked_bidders_guids = []

        # Meta fields in an event log
        self.media_guid = ""
        self.device_type = ""
        self.device_os = ""
        self.os = ""
        self.user_tracking_type = ""
        self.is_using_user_tracker_id_session_UUID = ""
        self.vpaid_type = ""
        self.io_guid = ""
        self.media_type = ""
        self.media_sub_type = ""
        self.filter_reasons_v2 = ""
        self.filter_reasons = ""
        self.filter_reason = ""
        self.winnerBidder: Bidder = None
        self.loserBidders = []
        self.winner_id = ""
        self.result = ""
        self.episode = ""
        self.title = ""
        self.series = ""
        self.genre = ""
        self.categories = ""
        self.productionQuality = ""
        self.mediaRating = ""
        self.liveStream = ""
        self.length = ""
        self.language = ""
        self.impExp = ""
        self.loss_reason_code = ""
        self.impId = ""
        self.wcpm = ""
        self.bid_win = ""
        self.partner_demand_fee_percentage = ""


class EventType(Enum):
    RTB_EVENT = "Send rtbEvent "  # rtb opportunity event̵̵̵
    VIDEOTRUEFIRSTCALL = "Sending Event:VIDEOTRUEFIRSTCALL"  # opportunity event
    demandopportunity = "Sending Event:demandopportunity"  # demand opportunity event
