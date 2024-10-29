import os


class Configuration:
    """Class that is has all external(env) configurations already loaded"""

    def __init__(self):
        self.local_log_reader_path_delivery = os.getenv("READ_LOG_PATH_DELIVERY")
        self.local_log_reader_path_events = os.getenv("READ_LOG_PATH_EVENTS")
        self.read_log_strategy = os.getenv("READ_LOG_STRATEGY")
        self.media_server_path = os.getenv("DF_MEDIA_SERVER_URL")

        # logReaderOpenSearch.py
        self.host_open_search = os.getenv(
            "READ_LOG_OPEN_SEARCH_HOST", "CHANGE_ENV_READ_LOG_OPEN_SEARCH_HOST"
        )

        self.open_search_port = int(os.getenv("READ_LOG_OPEN_SEARCH_PORT", "443"))

        self.root_domain = os.getenv("COMPANY_ROOT_DOMAIN", "siprocalads.com")

        self.open_search_time_to_wait_to_read_delivery_tid = int(
            os.getenv("DF_CONFIG_TIME_TO_WAIT_TO_READ_LOG_DELIVERY_TID", "5")
        )

        self.open_search_time_to_wait_to_read_quartz = int(
            os.getenv("DF_CONFIG_TIME_TO_WAIT_TO_READ_LOG_QUARTZ", "3")
        )

        self.open_search_time_to_wait_to_read_delivery = int(
            os.getenv("DF_CONFIG_TIME_TO_WAIT_TO_READ_LOG_DELIVERY", "0")
        )

        self.open_search_max_times_retry_find_tid = int(
            os.getenv("DF_CONFIG_MAX_RETRY_TO_FIND_TID", "5")
        )

        self.open_search_wait_time_on_retry_for_tid = int(
            os.getenv("DF_CONFIG_WAIT_TIME_RETRY_TO_FIND_TID", "10")
        )

        self.rtb_tmax = int(os.getenv("DELIVERY_RTB_TMAX", "300"))

        self.open_search_time_to_wait_to_read_event_tid = int(
            os.getenv("TIME_TO_WAIT_TO_READ_LOG_EVENT_TID", "5")
        )

        self.open_search_time_to_wait_to_read_event_log = int(
            os.getenv("TIME_TO_WAIT_TO_READ_EVENT_LOG", "0")
        )

        self.open_search_time_to_wait_to_read_event_log_2ndTime = int(
            os.getenv("TIME_TO_WAIT_TO_READ_EVENT_LOG_2ndTIME", "1")
        )

        self.dashboard_api = os.getenv("DSE_DASHBOARD_API")
        self.api_user = os.getenv("DSE_API_USER")
        self.api_pwd = os.getenv("DSE_API_PWD")
        self.environment = os.getenv("DSE_ENVIRONMENT")

        self.read_event_logs = False
