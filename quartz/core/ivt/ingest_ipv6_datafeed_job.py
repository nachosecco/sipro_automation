import os
from core.ivt.ingest_ivt_datafeed_job import IngestIVTDataFeedJob

class IngestIPv6DataFeedJob(IngestIVTDataFeedJob):
	def __init__(self):
		fs_sub_folder = os.environ.get(
			"QRT_IVT_IPv6_SUB_FOLDER", "/upload/ipv6blocklist"
		)
		IngestIVTDataFeedJob.__init__(self, fs_sub_folder)
		self.job_name = "pixalate.IngestIPv6DatafeedJob"
		self.source_filename_prefix = "regression_ipv6_"
		self.redis_key_prefix = "IPV6:"
		self.file_key_col_name = "ip"

	def upload_data_to_fs(self):
		file_header = "ip,ipType,fraudType,probability\n"
		file_line_format = "%s,GlobalUnicast,%s,0.3293234\n"

		for file in self.data_files:
			file_data = file_header
			for record in file["records"]:
				file_data += file_line_format % (record[self.file_key_col_name], record["fraudType"])
			self.fs.write_data(bytes(file_data, 'utf-8'), str(file["filename"]).strip())
