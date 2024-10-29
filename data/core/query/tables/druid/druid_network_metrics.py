from dataclasses import dataclass

from core.query.tables.druid.druid_common_metrics import CommonMetricsDruid


@dataclass
class NetworkMetricsDruid(CommonMetricsDruid):
    """Metrics that are used in Network table"""

    OPPORTUNITY = "opportunity"
    T_REVENUE = "trevenue"
    G_REVENUE = "grevenue"
    CLICKS = "clicks"
    POTENTIAL_TO_FILL = "potentialtofill"
