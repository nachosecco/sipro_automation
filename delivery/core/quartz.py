import os
import requests


class Quartz:
    """This class represent the quartz job executions"""

    def __init__(self, quartz_api, logger):
        self.quartz_api = quartz_api
        self.quartz_run_job_timeout = int(os.environ.get("DFQ SERVER_ROOT_TIME_OUT", 5))
        self.logger = logger

    def run_job(self, job_name):
        url = self.quartz_api
        try:
            if not url.endswith("/"):
                url = f"{url}/"
            url = f"{url}run?key={job_name}"
            response = requests.get(url, timeout=60000)
        except:
            self.logger.error(
                f"Error on call to execution of job [{job_name}] with api url[{url}]]"
            )
            return False

        if response.status_code != 200:
            self.logger.error(
                f"Error while running Quartz job {job_name}. Status should be 200 but got {response.status_code}"
            )
            return False

        if "No Job Found" in response.text:
            self.logger.error(
                f"Error while running Quartz job {job_name}. Job not found"
            )
            return False

        if "Job Failed" in response.text:
            self.logger.error(
                f"Error while running Quartz job {job_name}. Job Failed to run"
            )
            return False

        return True
