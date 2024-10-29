from core.utils.app_utils import check_and_get_env


class Configuration:
    """Class to get configuration parameters from environmental variables"""

    def __init__(self):
        self.athena_database = check_and_get_env("DSE_ENVIRONMENT").lower()
        self.s3_mapr_bucket = check_and_get_env("S3_MAPR_BUCKET_NAME").lower()
        self.aws_region = check_and_get_env("AWS_REGION").lower()
        self.mwaa_environment_name = check_and_get_env("MWAA_ENVIRONMENT_NAME").lower()
