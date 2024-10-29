from dataclasses import dataclass

from core.query.tables.druid.druid_common_metrics import CommonMetricsDruid


@dataclass
class CampaignMetricsDruid(CommonMetricsDruid):
    """Metrics that are used in Druid table"""

    ATTEMPTS = "attempts"
    DEMAND_OPPS = "demand_opps"
    GREVENUE = "grevenue"
    CLICKS = "clicks"
