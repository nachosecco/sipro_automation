import os
from core.ivt.ingest_ivt_datafeed_job import IngestIVTDataFeedJob

class IngestUADatafeedJob(IngestIVTDataFeedJob):
	def __init__(self):
		fs_sub_folder = os.environ.get(
			"QRT_IVT_UA_SUB_FOLDER", "/upload/useragentlistv2"
		)
		IngestIVTDataFeedJob.__init__(self, fs_sub_folder)
		self.job_name = "pixalate.IngestUserAgentDatafeedJob"
		self.source_filename_prefix = "regression_ua_"
		self.redis_key_prefix = "UA:"
		self.file_key_col_name = "line"

	def upload_data_to_fs(self):
		for file in self.data_files:
			file_data = ""
			for record in file["records"]:
				file_data += record[self.file_key_col_name] + "\n"
			self.fs.write_data(bytes(file_data, 'utf-8'), str(file["filename"]).strip())
