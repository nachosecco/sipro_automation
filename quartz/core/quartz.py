import os
import requests

class Quartz:
	def __init__(self):
		self.protocol = os.environ.get('QRT_QUARTZ_PROTOCOL', 'http')
		self.host = os.environ.get('QRT_QUARTZ_HOST', 'localhost')
		self.port = os.environ.get('QRT_QUARTZ_PORT', '8060')
		self.timeout = int(os.environ.get('QRT_QUARTZ_TIMEOUT', 300))

	def run_job(self, job_name):
		response = requests.get(f"{self.protocol}://{self.host}:{self.port}/run", params={'key': job_name}, timeout=self.timeout)

		if response.status_code != 200:
			raise Exception(f"Error running Quartz job {job_name}")
		elif "No Job Found" in response.text:
			raise Exception(f"Quartz job {job_name} not found")
		elif "Job Failed" in response.text:
			raise Exception(f"Quartz job {job_name} failed to run")
		# TODO: We need a way to know if it doesn't run because it is already running
