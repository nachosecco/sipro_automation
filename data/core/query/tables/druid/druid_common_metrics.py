from dataclasses import dataclass


@dataclass
class CommonMetricsDruid:
    """Common metrics in druid tables"""

    MOAT_AUD = "moat_aud"
    IMPRESSION = "impression"
    REVENUE = "revenue"
    QUARTILE0 = "quartile0"
    QUARTILE25 = "quartile25"
    QUARTILE50 = "quartile50"
    QUARTILE75 = "quartile75"
    QUARTILE100 = "quartile100"
    OPEN_VIDEO_VIABILITY = "openvideoviewability"
    DEMAND_PARTNER_FEE = "demandPartnerFee"
