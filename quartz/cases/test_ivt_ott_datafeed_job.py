import unittest
from core.ivt.ingest_ott_datafeed_job import IngestOTTDataFeedJob


def test_loads_ott_data_to_redis():
	"""
	Given a OTT block list file
	After job execution
	The blocked ips should be present in the redis
	"""
	device_id = "472db8de-bd28-5722-80b7-cade19faf793"
	with IngestOTTDataFeedJob() as test:
		records = [
			{
				"deviceId": device_id,
				"fraudType": "sample"
			}
		]
		test.add_file(records)
		test.execute()

		# Search for record with invalid key and it's not found
		value = test.get_record_by_key("sample")
		unittest.TestCase().assertIsNone(value)

		# Search for record with valid key and element is found
		# Confirms key is created using ip value
		value = test.get_record_by_key(device_id)
		unittest.TestCase().assertIsNotNone(value)
