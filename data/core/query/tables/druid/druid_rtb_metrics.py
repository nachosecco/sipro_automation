from dataclasses import dataclass

from core.query.tables.druid.druid_common_metrics import CommonMetricsDruid


@dataclass
class RTBMetricsDruid(CommonMetricsDruid):
    """Metrics that are used in RTB Hourly table"""

    BIDS = "bids"
    DSP_BIDS = "dsp_bids"
    DSP_BID_WINS = "dsp_bid_wins"
    TCP_ERRORS = "tcp_errors"
    CLICK = "click"
    B_REVENUE = "brevenue"
    W_REVENUE = "wrevenue"
    RESPONSE_TIME = "responsetime"
    ERRORS = "errors"
    TIMEOUTS = "timeouts"
    RTB_OPPS = "rtb_opps"
    DEAL_OPPS = "deal_opps"
    SEAT_OPPS = "seat_opps"
    RTB_BIDS = "rtb_bids"
    DEAL_BIDS = "deal_bids"
    SEAT_BIDS = "seat_bids"
    ATTEMPTS = "attempts"
