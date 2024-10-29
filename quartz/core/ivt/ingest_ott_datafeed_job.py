import os
from core.ivt.ingest_ivt_datafeed_job import IngestIVTDataFeedJob

class IngestOTTDataFeedJob(IngestIVTDataFeedJob):
	def __init__(self):
		fs_sub_folder = os.environ.get(
			"QRT_IVT_OTT_SUB_FOLDER", "/upload/ottblocklist"
		)
		IngestIVTDataFeedJob.__init__(self, fs_sub_folder)
		self.job_name = "pixalate.IngestOTTDatafeedJob"
		self.source_filename_prefix = "regression_ott_"
		self.redis_key_prefix = "OTT:"
		self.file_key_col_name = "deviceId"

	def upload_data_to_fs(self):
		file_header = "deviceId,fraudType,os,ifaType,deviceName,probability\n"
		file_line_format = "%s,%s,android,AFAI,Amazon,0.541507483626598\n"

		for file in self.data_files:
			file_data = file_header
			for record in file["records"]:
				file_data += file_line_format % (record[self.file_key_col_name], record["fraudType"])
			self.fs.write_data(bytes(file_data, 'utf-8'), str(file["filename"]).strip())
