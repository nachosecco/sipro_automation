from dataclasses import dataclass

from core.query.tables.druid.druid_table import druid_table


@dataclass
@druid_table("campaign_v5")
class DruidTableCampaign:
    """Class to represent the table for the campaign table"""
