import logging
import requests
import time
from datetime import datetime
import boto3
from core.constants import DATA_MONITOR_HOUR_PARAM

# Constants
START_DATE_GTE_PARAM = (
    "start_date_gte"  # Airflow parameter to filter runs by execution time
)
DAG_STATUS_POLL_INTERVAL = 5  # seconds


class AirflowClient:
    """This class authenticates and communicates with the Airflow Rest API"""

    def __init__(self, region_name, env_name):
        self.region_name = region_name
        self.env_name = env_name
        # Store the current time for use in our later queries to filter runs by execution time
        self.run_datetime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # Create a session object to store the cookies
        self.session = requests.session()

        logging.info(
            f"Initializing Airflow Client for environment {self.env_name} at region {self.region_name}"
        )

        # Initialize MWAA client and request a web login token
        mwaa = boto3.client("mwaa", region_name=self.region_name)

        response = mwaa.create_web_login_token(Name=self.env_name)

        # Extract the web server hostname and login token
        web_server_host_name = response["WebServerHostname"]
        web_token = response["WebToken"]

        # Construct the URL needed for authentication
        login_url = f"https://{web_server_host_name}/aws_mwaa/login"
        login_payload = {"token": web_token}

        # Make a POST request to the MWAA login url using the login payload
        response = self.session.post(login_url, data=login_payload, timeout=10)

        # Check if login was successful
        if response.status_code == 200:
            # Store the hostname
            self.web_server_host_name = web_server_host_name
            # Add cookie to the session. It will be automatically sent with subsequent requests that use the session
            self.session.cookies.update(response.cookies)
        else:
            raise Exception("Failed to log in: HTTP %d", response.status_code)

    def trigger_dag(self, dag_id, conf):
        # Construct the URL and json body for triggering a DAG
        url = f"https://{self.web_server_host_name}/api/v1/dags/{dag_id}/dagRuns"
        json_body = {"conf": conf}

        response = self.session.post(url, json=json_body)

        if response.status_code == 200:
            new_dag_run = response.json()
            return new_dag_run

        # If the DAG failed to trigger, raise an exception
        raise Exception(
            f"Failed to trigger DAG: HTTP {response.status_code} - {response.text}"
        )

    def get_dag_run_by_dag_run_id(self, dag_id, dag_run_id):
        # Construct the URL for checking the status of a DAG run
        url = f"https://{self.web_server_host_name}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}"
        response = self.session.get(url)

        if response.status_code == 200:
            dag_run_response = response.json()
            return dag_run_response

        # If we didn't find the DAG run, raise an exception
        raise Exception(
            f"Failed to get DAG run for dag_id: {dag_id} and dag_run_id: {dag_run_id}"
        )

    def find_dag_run_by_etl_hour(self, dag_id, etl_hour):
        # Construct the URL for listing all DagRuns for a specific DAG
        url = f"https://{self.web_server_host_name}/api/v1/dags/{dag_id}/dagRuns"
        response = self.session.get(
            url,
            # Only look for DagRuns that started after we instantiate the class at the beginning of a test run
            params={START_DATE_GTE_PARAM: self.run_datetime},
        )

        if response.status_code == 200:
            # Find the DagRun with conf that matches the ETL hour
            for dag_run in response.json()["dag_runs"]:
                if dag_run["conf"][DATA_MONITOR_HOUR_PARAM] == etl_hour:
                    return dag_run

        # If we didn't find the DagRun, raise an exception
        raise Exception(
            f"Failed to find DagRun for Dag: {dag_id} with ETL hour: {etl_hour}"
        )

    def wait_for_dag_run_completion(self, dag_id, dag_run_id):
        """Wait for the DAG run to complete by polling the dagRun endpoint until the status changes to success or failed
        :param dag_id: target dag id
        :param dag_run_id: target dag run id
        :return: True if the DAG run completed successfully, False if it failed
        """
        logging.info(
            f"Waiting for DAG run completion for dag_id: {dag_id} and dag_run_id: {dag_run_id}"
        )

        # Poll the dagRun endpoint until the status changes to success or failed
        while True:
            # Check the status of the DAG run
            dag_run_response = self.get_dag_run_by_dag_run_id(dag_id, dag_run_id)
            if dag_run_response["state"] == "success":
                logging.debug(
                    f"DAG run completed successfully: {dag_id} - {dag_run_id}"
                )
                return True
            elif dag_run_response["state"] == "failed":
                logging.error(f"DAG run failed: {dag_id} - {dag_run_id}")
                return False
            else:
                logging.debug(f"DAG run still in progress: {dag_id} - {dag_run_id}")
                # Wait for a few seconds before checking again
                time.sleep(DAG_STATUS_POLL_INTERVAL)
