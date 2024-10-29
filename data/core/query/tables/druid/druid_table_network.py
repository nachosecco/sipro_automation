from dataclasses import dataclass

from core.query.tables.druid.druid_table import druid_table


@dataclass
@druid_table("network_v1")
class DruidTableNetwork:
    """Class to represent the table for the network table"""
