import os
import time

from core.RoutersConstants import AF_ID_INVENTORY_ROUTERS_INDIVIDUAL
from core.configuration import Configuration
from core.openSearchHelper import OpenSearchHelper


# Class to read a Log from Open Search
class LogReaderIRSFromOpenSearch:
    def __init__(self, id_automation_framework, external_config):
        self.id_automation_framework = id_automation_framework
        self.thread_to_find = ""
        self.event_thread_to_find = ""
        self.inventory_routers_thread_to_find = ""
        self.config = (
            external_config if external_config is not None else Configuration()
        )

    # Create an instance of search helper using env variables
    def open_search(self, app_name: str):
        host_open_search = self.config.host_open_search
        if (
            host_open_search == "CHANGE_ENV_READ_LOG_OPEN_SEARCH_HOST"
            or host_open_search is None
        ):
            raise Exception("READ_LOG_OPEN_SEARCH_HOST is a variable that is required")

        return OpenSearchHelper(
            host_open_search, self.config.open_search_port, app_name
        )

    def find_logs_inventory_routers(self):
        open_search_helper = self.open_search("app-web-inventoryrouters*")
        found_first_call = open_search_helper.search_tid_by_message(
            f"{AF_ID_INVENTORY_ROUTERS_INDIVIDUAL}={self.id_automation_framework}"
        )

        if len(found_first_call) == 0:
            time.sleep(self.config.open_search_time_to_wait_to_read_delivery_tid)

            found_first_call = open_search_helper.search_tid_by_message(
                f"{AF_ID_INVENTORY_ROUTERS_INDIVIDUAL}={self.id_automation_framework}"
            )

        assert not (len(found_first_call) == 0)

        self.inventory_routers_thread_to_find = str(found_first_call[0])

        logs = open_search_helper.search_message_by_tid(
            self.inventory_routers_thread_to_find
        )

        return logs


class LogReader:
    def __init__(self, automation_router_uid: str, external_config=None):
        self.automation_router_uid = automation_router_uid
        self.config = external_config
        self.reader = self.__log_reader_strategy()

    def __log_reader_strategy(self):
        strategy = os.getenv("READ_LOG_STRATEGY", None)
        if strategy == "CHANGE_ENV_VAR_READ_LOG_STRATEGY":
            raise Exception(
                'READ_LOG_STRATEGY is a variable that is required, valid values are ("OPEN_SEARCH"'
            )

        if strategy == "OPEN_SEARCH":
            return LogReaderIRSFromOpenSearch(self.automation_router_uid, self.config)

        raise Exception('Invalid READ_LOG_STRATEGY, valid values are ("OPEN_SEARCH"')

        pass

    def find_logs_inventory_routers(self):
        return self.reader.find_logs_inventory_routers()
