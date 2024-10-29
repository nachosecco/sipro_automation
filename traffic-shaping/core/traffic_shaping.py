import uuid
from typing import List

from core.configuration import Configuration
from core.models.traffic_shaping_record import TrafficShapingRecord
from core.query.athena import execute_queries
from core.s3 import S3
from core.utils.insert_statement_builder import (
    RTBInsertStatementBuilder,
    ImpressionInsertStatementBuilder,
)
from core.utils.airflow_client import AirflowClient
from core.constants import (
    DATA_MONITOR_JOB_NAME,
    DATA_AGGREGATOR_JOB_NAME,
    BLOCKLIST_GENERATOR_JOB_NAME,
    DATA_MONITOR_HOUR_PARAM,
    LAST_PROCESSED_FILE_NAME_PARAM,
    AUTOMATION_LAST_PROCESSED_FILE_DIRECTORY,
)
from core.utils.date_utils import get_past_hours


class TrafficShaping:
    def __init__(
        self,
        data_monitor_hour_records: [TrafficShapingRecord],
        blocked_records: List[TrafficShapingRecord],
        allowed_records: List[TrafficShapingRecord],
        data_monitor_hour: str,
        last_24_hours: [],
        configuration: Configuration,
        record_uuid: str,
    ):
        self.data_monitor_hour_records = data_monitor_hour_records
        self.blocked_records = blocked_records
        self.allowed_records = allowed_records
        self.configuration = configuration
        self.data_monitor_hour = data_monitor_hour
        self.last_24_hours = last_24_hours
        self.record_uuid = record_uuid
        self.airflow_client = AirflowClient(
            configuration.aws_region, configuration.mwaa_environment_name
        )

    def seed_data(self):
        # Seed data to athena rtb and impression tables by executing the insert statements
        queries = [
            self.__create_rtb_insert_statement(),
            self.__create_impression_insert_statement(),
        ]

        execute_queries(
            self.configuration.athena_database,
            queries,
        )

    def __create_rtb_insert_statement(self):
        return RTBInsertStatementBuilder.create_insert_statement(
            [
                self.data_monitor_hour_records,
                self.blocked_records,
                self.allowed_records,
            ]
        )

    def __create_impression_insert_statement(self):
        return ImpressionInsertStatementBuilder.create_insert_statement(
            self.allowed_records
        )

    @staticmethod
    def init_from_records(
        hourly_records: dict,
        data_monitor_hour: str,
        configuration: Configuration,
        placement_guid: str,
        app_bundle_id: str,
    ):
        data_monitor_hour_records, blocked_records, allowed_records = [], [], []
        # Generate unique identifiers for the placement and app to ensure data isolation
        record_uuid = str(uuid.uuid4())

        # Generate only one record for the data_monitor_hour to be used by traffic shaping data monitor job
        if data_monitor_hour is not None:
            transaction_guid = "transaction_" + str(uuid.uuid4())
            data_monitor_hour_records.append(
                TrafficShapingRecord(
                    bidder_guid="data_monitor_hour_bidder",
                    hour=data_monitor_hour,
                    placement_guid=placement_guid,
                    app_bundle_id=app_bundle_id,
                    transaction_guid=transaction_guid,
                )
            )

        last_24_hours = []
        # Iterate through each hour record and populate it with data that will result in allowed or blocked bidders
        for etl_hour, bidders in hourly_records.items():
            last_24_hours.append(etl_hour)
            for bidder_type, bidder_guids in bidders.items():
                for bidder_guid in bidder_guids:
                    transaction_guid = "transaction_" + str(uuid.uuid4())
                    record = TrafficShapingRecord(
                        bidder_guid=bidder_guid,
                        hour=etl_hour,
                        placement_guid=placement_guid,
                        app_bundle_id=app_bundle_id,
                        transaction_guid=transaction_guid,
                    )
                    if bidder_type == "blocked":
                        blocked_records.append(record)
                    else:
                        allowed_records.append(record)

        return TrafficShaping(
            data_monitor_hour_records,
            blocked_records,
            allowed_records,
            data_monitor_hour,
            last_24_hours,
            configuration,
            record_uuid,
        )

    def __generate_last_processed_file_name(self, file_name):
        # Generate a unique last processed file name using a timestamp to avoid conflicts
        return f"{AUTOMATION_LAST_PROCESSED_FILE_DIRECTORY}/{file_name}.txt"

    def cleanup_records(self, case_name):
        # Deletes folders and files related to traffic shaping from S3.
        hive_subfolder = "user/hive/warehouse"
        s3 = S3(self.configuration.s3_mapr_bucket)
        s3.delete_folder(f"{hive_subfolder}/rtb/hour={self.data_monitor_hour}")
        for hour in self.last_24_hours:
            s3.delete_folder(f"{hive_subfolder}/rtb/hour={hour}")
            s3.delete_folder(f"{hive_subfolder}/impression/hour={hour}")

        s3.delete_files(
            [f"traffic-shaping/{self.__generate_last_processed_file_name(case_name)}"]
        )

    def __find_and_wait_for_dag_run_completion(self, dag_id, etl_hour):
        # Find the dag run for the given etl_hour
        dag_run = self.airflow_client.find_dag_run_by_etl_hour(dag_id, etl_hour)
        # Extract the dag run id
        dag_run_id = dag_run["dag_run_id"]
        # Wait for the dag run to complete
        self.airflow_client.wait_for_dag_run_completion(dag_id, dag_run_id)

    def trigger_dags_and_wait_for_completion(self, data_monitor_hour, test_case_name):
        prior_hours = get_past_hours(data_monitor_hour)
        # Trigger Data Monitor Job
        job_conf = {
            DATA_MONITOR_HOUR_PARAM: data_monitor_hour,
            LAST_PROCESSED_FILE_NAME_PARAM: self.__generate_last_processed_file_name(
                test_case_name
            ),
        }
        data_monitor_dag_run = self.airflow_client.trigger_dag(
            DATA_MONITOR_JOB_NAME, job_conf
        )

        # Wait for Data Monitor job to complete
        data_monitor_dag_run_id = data_monitor_dag_run["dag_run_id"]
        self.airflow_client.wait_for_dag_run_completion(
            DATA_MONITOR_JOB_NAME, data_monitor_dag_run_id
        )

        # Wait for the Data Aggregator job for the prior hour to complete
        self.__find_and_wait_for_dag_run_completion(
            DATA_AGGREGATOR_JOB_NAME, prior_hours[0]
        )

        # Wait for the Blocklist Generator job for the prior hour to complete
        self.__find_and_wait_for_dag_run_completion(
            BLOCKLIST_GENERATOR_JOB_NAME, prior_hours[0]
        )
