from dataclasses import dataclass

from core.query.tables.druid.druid_table import druid_table


@dataclass
@druid_table("rtb_v6")
class DruidTableRTB:
    """Class to represent the table for the rtb table"""
