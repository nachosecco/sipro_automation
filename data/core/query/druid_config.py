from core.util.app_utils import check_and_get_env


class DruidConfig:
    """It has the information to connect to druid"""

    def __init__(self):
        self.druid_username = check_and_get_env("DPR_DRUID_USERNAME")
        self.druid_password = check_and_get_env("DPR_DRUID_PASSWORD")
        self.druid_timeout = int(check_and_get_env("DPR_DRUID_TIMEOUT"))
        host = check_and_get_env("DPR_DRUID_URL")
        self.druid_url = f"https://{host}/druid/v2/sql/"
