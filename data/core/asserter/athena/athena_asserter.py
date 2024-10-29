import logging

from core.query.tables.athena.athena_table_common import AthenaTableCommon
from core.query.tables.athena.athena_table_impression import AthenaTableImpression
from core.query.tables.athena.athena_table_open_video_viability import (
    AthenaTableOpenVideoViability,
)
from core.query.tables.athena.athena_table_opportunity import AthenaTableOpportunity
from core.query.tables.athena.athena_table_rtb import AthenaTableRTB
from core.query.athena import query, count_query, sum_query


def to_athena_hour(date):
    date_str, time_str = date.split()
    time_str = time_str[:2]
    date_str = date_str.replace("-", "")
    return date_str, time_str


def to_athena_start_hour(date):
    date_str, time_str = to_athena_hour(date)
    return f"{date_str}_{time_str}00"


def to_athena_end_hour(date):
    date_str, time_str = to_athena_hour(date)
    return f"{date_str}_{time_str}59"


def query_assert(database, sql, expected_value):
    ans = query(database, sql)
    count_or_sum = ans["ResultSet"]["Rows"][1]["Data"][0]["VarCharValue"]

    logging.info(f"\nAthena response: {count_or_sum}\n")
    if int(count_or_sum) != expected_value:
        raise Exception(
            f" Athena value {count_or_sum} doesn't match expected value {expected_value}."
        )


def query_assert_float(database, sql, expected_value, precision):
    ans = query(database, sql)
    rows = ans["ResultSet"]["Rows"]
    rows_len = len(rows)
    expected_value_len = len(expected_value)
    logging.info(f"\nAthena response: {rows}\n")
    if rows_len - 1 != expected_value_len:
        raise Exception(
            f"Returned Athena rows {rows_len - 1} doesn't match expected rows {expected_value_len}."
        )
    for idx, row in enumerate(rows):
        if idx == 0:
            continue
        for idx_field, field in enumerate(row["Data"]):
            if "VarCharValue" in field:
                crt = float(field["VarCharValue"])
                val = expected_value[idx - 1][idx_field]
                crt_rounded = round(crt, precision)
                val_rounded = round(val, precision)
                if crt_rounded != val_rounded:
                    raise Exception(
                        f"Rounded value from Athena {crt_rounded} does not match expected rounded value {val_rounded}. At row {idx - 1} and col {idx_field}."
                    )
                continue
            raise Exception(
                f"Row doesn't have VarCharValue. It could mean, "
                f"the returned records from Athena is empty."
            )


class AthenaAsserter:
    """Assertions to athena tables"""

    def __init__(self, case):
        self.case = case

    def opportunity(self):
        return AthenaAsserterTable(self.case, AthenaTableOpportunity())

    def rtb(self):
        return AthenaAsserterTable(self.case, AthenaTableRTB())

    def open_video_viability(self):
        return AthenaAsserterTable(self.case, AthenaTableOpenVideoViability())

    def impression(self):
        return AthenaAsserterTable(self.case, AthenaTableImpression())


class AthenaAsserterTable:
    """Table to do assertions to athena table"""

    def __init__(self, case, table: AthenaTableCommon):
        self.case = case
        self.table = table

    def query_of_sum_metrics_with_single_row_equals_to(
        self, metrics: list, expected_values: list
    ):
        self.query_of_sum_metrics_and_dimensions_with_single_row_equals_to(
            metrics, [], expected_values
        )

    def query_of_count_equals_to(self, expected_value: int):
        table_name, placement = self.extract_pre_query_info()
        sql = count_query(
            table_name,
            to_athena_start_hour(self.case.context.min_hour),
            to_athena_end_hour(self.case.context.max_hour),
            placement,
        )
        logging.info(f"Athena SQL:\n-----------\n{sql}\n-----------")
        query_assert(self.case.configuration.athena_database, sql, expected_value)

    def query_of_sum_metrics_and_dimensions_with_single_row_equals_to(
        self, metrics: list, dimensions: list, expected_values: list, precision=3
    ):
        self.query_of_sum_metrics_and_dimensions_with_equals_to(
            metrics, dimensions, [expected_values], precision
        )

    def query_of_sum_metrics_and_dimensions_with_equals_to(
        self, metrics: list, dimensions: list, expected_values, precision=3
    ):
        table_name, placement = self.extract_pre_query_info()
        sql = sum_query(
            table_name,
            metrics,
            dimensions,
            to_athena_start_hour(self.case.context.min_hour),
            to_athena_end_hour(self.case.context.max_hour),
            placement,
        )
        logging.info(f"Athena SQL:\n-----------\n{sql}\n-----------")
        query_assert_float(
            self.case.configuration.athena_database, sql, expected_values, precision
        )

    def extract_pre_query_info(self):
        table_name = self.table.meta_athena_table["name"]
        placement = self.case.delivery_parameters.uid

        return table_name, placement
