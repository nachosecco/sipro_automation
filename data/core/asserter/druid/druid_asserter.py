import json
import logging

from core.data_exception import DataException
from core.query.druid import query_sql
from core.query.druid_config import DruidConfig
from core.query.query_templates import create_druid_query, create_druid_count_query
from core.query.tables.druid.druid_network_dimensions import NetworkDimensionsDruid
from core.query.tables.druid.druid_table_campaign import (
    DruidTableCampaign,
)
from core.query.tables.druid.druid_table_network import DruidTableNetwork
from core.query.tables.druid.druid_table_rtb import DruidTableRTB


def assert_table(expected_values, rows):
    for i, e in enumerate(expected_values):
        for j, c in enumerate(e):
            crt = rows[i][j]
            if isinstance(crt, float):
                if round(crt, 3) != round(c, 3):
                    raise DataException(
                        f"Druid value {crt} does not match expected value {c}. Index: [{i}, {j}]."
                    )
            elif crt != c:
                raise DataException(
                    f"Druid value {crt} does not match expected value {c}. Index: [{i}, {j}]."
                )


def assert_sql(sql: str, expected_values):
    logging.info("SQL: \n-----------\n%s\n-----------", sql)
    druid_config = DruidConfig()
    response = query_sql(
        druid_config.druid_url,
        druid_config.druid_username,
        druid_config.druid_password,
        sql,
    )
    logging.info(f"\nDruid response: {response}\n")
    rows = json.loads(response)

    assert_table(expected_values, rows)


class DruidAsserter:
    """Class to start asserting in druid"""

    def __init__(self, case):
        self.case = case

    def rtb(self):
        return DruidAsserterTable(self.case, DruidTableRTB())

    def network(self):
        return DruidAsserterTable(self.case, DruidTableNetwork())

    def campaign(self):
        return DruidAsserterTable(self.case, DruidTableCampaign())


class DruidAsserterTable:
    """class to common methods to assert data"""

    def __init__(self, case, table):
        self.case = case
        self.table = table

    def query_of_count_equals_to(self, expected_value):
        table_name, placement = self.extract_pre_query_info()

        sql = create_druid_count_query(
            table_name,
            self.case.context.min_hour,
            self.case.context.max_hour,
            placement,
        )

        assert_sql(sql, expected_value)

    def query_of_sum_metrics_with_single_row_equals_to(self, metrics, expected_values):
        self.query_of_sum_metrics_and_dimensions_with_single_row_equals_to(
            metrics, [], expected_values
        )

    def query_of_sum_metrics_and_dimensions_with_single_row_equals_to(
        self, metrics, dimensions, expected_values
    ):
        self.query_of_metrics_and_dimensions_with_equals_to(
            metrics, dimensions, [expected_values]
        )

    def query_of_sum_metrics_and_dimensions_with_equals_to(
        self, metrics, dimensions, expected_values
    ):
        self.query_of_metrics_and_dimensions_with_equals_to(
            metrics, dimensions, expected_values
        )

    def query_of_metrics_and_dimensions_with_equals_to(
        self, metrics, dimensions, expected_values
    ):
        table_name, placement = self.extract_pre_query_info()

        filters = [{"dimension": NetworkDimensionsDruid.PLACEMENT, "value": placement}]

        sql = create_druid_query(
            table_name,
            metrics,
            dimensions,
            filters,
            self.case.context.min_hour,
            self.case.context.max_hour,
            [],
            len(expected_values),
        )

        assert_sql(sql, expected_values)

    def extract_pre_query_info(self):
        table_name = self.table.meta_druid_table["name"]
        placement = self.case.delivery_parameters.uid

        return table_name, placement
