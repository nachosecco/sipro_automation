import json
from typing import List

from core.models.traffic_shaping_record import TrafficShapingRecord


def flatten_list_of_queries(list_of_lists):
    return [query for sublist in list_of_lists for query in sublist]


class InsertStatementBuilderBase:
    @staticmethod
    def create_insert_statement_athena_table(keys, values, table_name):
        columns = ", ".join(keys)
        values = ", ".join(values)
        return f"INSERT INTO {table_name} ({columns}) VALUES {values}"

    @staticmethod
    def create_values_record_for_insert_statement(data):
        values = ", ".join(f"'{v}'" for v in data.values())
        return f"({values})"


class RTBInsertStatementBuilder(InsertStatementBuilderBase):
    @staticmethod
    def create_insert_statement(records_list):
        table_name = "rtb"
        query_values = [
            RTBInsertStatementBuilder.create_insert_value_strings(records)
            for records in records_list
        ]

        return RTBInsertStatementBuilder.create_insert_statement_athena_table(
            RTBInsertStatementBuilder.get_cols(),
            flatten_list_of_queries(query_values),
            table_name,
        )

    @staticmethod
    def create_insert_value_strings(records: List[TrafficShapingRecord]):
        # combines multiple records values into a string
        queries = []
        for record in records:
            app_meta = json.dumps({"appBundleId": record.app_bundle_id})
            bidders = RTBInsertStatementBuilder.__create_bidders_list(
                [record.bidder_guid]
            )
            data = {
                "transaction_guid": record.transaction_guid,
                "placement_guid": record.placement_guid,
                "app_meta": app_meta,
                "bidders": bidders,
                "hour": record.hour,
            }
            query = RTBInsertStatementBuilder.create_values_record_for_insert_statement(
                data
            )
            queries.append(query)
        return queries

    @staticmethod
    def __create_bidders_list(
        bidder_guids,
        template_path="./core/query/table_record_templates/bidders_template.json",
    ):
        with open(template_path) as f:
            template = json.load(f)
        bidders = {
            bidder_id: json.loads(
                json.dumps(template).replace("<BIDDER_GUID>", bidder_id)
            )
            for bidder_id in bidder_guids
        }
        return json.dumps(bidders)

    @staticmethod
    def get_cols():
        return [
            "transaction_guid",
            "placement_guid",
            "app_meta",
            "bidders",
            "hour",
        ]


class ImpressionInsertStatementBuilder(InsertStatementBuilderBase):
    @staticmethod
    def create_insert_statement(records):
        table_name = "impression"
        query_values = ImpressionInsertStatementBuilder.create_insert_value_strings(
            records
        )
        return ImpressionInsertStatementBuilder.create_insert_statement_athena_table(
            ImpressionInsertStatementBuilder.get_cols(),
            query_values,
            table_name,
        )

    @staticmethod
    def create_insert_value_strings(records: List[TrafficShapingRecord]):
        # combines multiple records values into a string

        queries = []
        for record in records:
            app_meta = json.dumps({"appBundleId": record.app_bundle_id})
            data = {
                "transaction_guid": record.transaction_guid,
                "placement_guid": record.placement_guid,
                "app_meta": app_meta,
                "cpm": "5.00",
                "demand_partner_fee": "0.00",
                "floor": "2.00",
                "hour": record.hour,
                "partner_guid": record.bidder_guid,
            }
            query = RTBInsertStatementBuilder.create_values_record_for_insert_statement(
                data
            )
            queries.append(query)
        return queries

    @staticmethod
    def get_cols():
        return [
            "transaction_guid",
            "placement_guid",
            "app_meta",
            "cpm",
            "demand_partner_fee",
            "floor",
            "hour",
            "partner_guid",
        ]
