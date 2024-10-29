import logging
import re
import time
from core.constants import AUTOMATION_FRAMEWORK_ID_DELIVERY
from core.exceptions import LogEntryNotFound
from core.openSearchHelper import OpenSearchHelper
from core.configuration import Configuration


# Class to read a Log from Open Search
class LogReaderFromOpenSearch:
    def __init__(
        self, id_automation_framework: str, configOverride: Configuration = None
    ):
        self.id_automation_framework = id_automation_framework
        self.tid = None
        self.thread_to_find = None
        self.event_thread_to_find = ""
        self.config = configOverride if configOverride is not None else Configuration()

    # Create an instance of search helper using env variables
    def open_search(self, app_name: str):
        host_open_search = self.config.host_open_search
        if host_open_search == "CHANGE_ENV_READ_LOG_OPEN_SEARCH_HOST":
            raise Exception("READ_LOG_OPEN_SEARCH_HOST is a variable that is required")

        return OpenSearchHelper(
            host_open_search, self.config.open_search_port, app_name
        )

    def find_logs_delivery(self, vpc):

        time.sleep(self.config.open_search_time_to_wait_to_read_delivery_tid)

        open_search_helper = self.open_search("app-web-delivery*")
        found_first_call = self.__find_tid_with_retry(open_search_helper, vpc)

        assert not (len(found_first_call) == 0)

        self.thread_to_find = str(found_first_call[0])

        logging.info("Tid =" + self.thread_to_find)

        thread_id = self.thread_to_find
        time_to_wait = self.config.open_search_time_to_wait_to_read_delivery

        if time_to_wait > 0:
            time.sleep(time_to_wait)

        logging.info("The tid that is used to find delivery logs is ==> " + thread_id)
        self.__find_logs_by_tid_with_retry(open_search_helper, thread_id)
        # running it twice to ensure all logs are available by now, instead of adding fixed sleep for every test
        # case, refer CP-2328
        time.sleep(1)
        found_logs = self.__find_logs_by_tid_with_retry(open_search_helper, thread_id)

        logging.info("The size that of delivery logs is ==> " + str(len(found_logs)))

        return found_logs

    def read_delivery(self, vpc, contains_to_test):
        found_logs = str(self.find_logs_delivery(vpc))

        return self.check_logs(contains_to_test, found_logs)

    def read_events(self, contains_to_test, event_logs):
        logs = str(event_logs)
        return self.check_logs(contains_to_test, logs)

    def set_tid(self, tid: str):
        self.tid = tid

    def find_logs_events(self):
        open_search_helper = self.open_search("app-web-event")
        time.sleep(self.config.open_search_time_to_wait_to_read_event_tid)
        transaction_guid = re.search("tx:(.+?) pl:", self.thread_to_find).group(1)
        message = f"transaction_guid: {transaction_guid}"
        found_first_call = self.__find_tid_by_message_with_retry(
            open_search_helper, message, 3
        )

        assert not (len(found_first_call) == 0)

        self.event_thread_to_find = thread_id = str(found_first_call[0])

        logging.info("Tid =" + self.event_thread_to_find)

        time.sleep(self.config.open_search_time_to_wait_to_read_event_log)
        self.__find_logs_by_tid_with_retry(open_search_helper, thread_id)
        time.sleep(self.config.open_search_time_to_wait_to_read_event_log_2ndTime)
        # running it twice to ensure all logs are available by now, instead of adding fixed sleep for every test
        # case, refer CP-2328
        found_logs = self.__find_logs_by_tid_with_retry(open_search_helper, thread_id)

        logging.debug("The size that of event logs is ==> " + str(len(found_logs)))
        return found_logs

    def find_logs_quartzalignment(self, text_to_search):
        logging.info(
            "The text used to find quartzalignment logs is ==> %s",
            text_to_search,
        )

        open_search_helper = self.open_search("app-web-quartzalignment")
        time.sleep(self.config.open_search_time_to_wait_to_read_quartz)
        found_logs = self.__find_logs_by_partial_message_search_with_retry(
            open_search_helper, text_to_search
        )

        logging.info("The size of found quartz logs is ==> %d", len(found_logs))

        return found_logs

    def check_logs(self, contains_to_test, logs: str):
        logging.debug(f"The size that of logs is ==> {len(logs)}")
        found_in_the_log = []
        for actual_log in contains_to_test:

            if logs.count(actual_log) > 0:
                found_in_the_log.append(actual_log)

        if not (len(contains_to_test) <= len(found_in_the_log)):
            logging.error(
                f"Expected logs ({contains_to_test}) the logs that were found were ({found_in_the_log})"
                f" and the actual log is  = > ({logs})"
            )

        return len(contains_to_test) <= len(found_in_the_log)

    def __find_tid_by_message_with_retry(
        self, open_search_helper, message: str, number_times_to_retry=0
    ):
        found_first_call = open_search_helper.search_tid_by_message(f"{message}")

        if found_first_call == "[tx: pl:]" or len(found_first_call) == 0:
            number_times_to_retry += 1
            if number_times_to_retry < 5:
                time.sleep(10)
                found_first_call = self.__find_tid_by_message_with_retry(
                    open_search_helper, message, number_times_to_retry
                )
            else:
                raise LogEntryNotFound(
                    f"TID for message [{message}] not found after {number_times_to_retry} retries"
                )

        return found_first_call

    def __find_tid_with_retry(self, open_search_helper, vpc, number_times_to_retry=0):
        if self.tid is not None:
            return [f"[tx:{self.tid} pl:{vpc.uid}]"]
        found_first_call = open_search_helper.search_tid_by_message(
            f"{AUTOMATION_FRAMEWORK_ID_DELIVERY}={self.id_automation_framework}"
        )

        max_times_retry_find_tid = self.config.open_search_max_times_retry_find_tid

        wait_time_on_retry_for_tid = self.config.open_search_wait_time_on_retry_for_tid

        if found_first_call == "[tx: pl:]" or len(found_first_call) == 0:
            number_times_to_retry += 1
            if number_times_to_retry < max_times_retry_find_tid:
                time.sleep(wait_time_on_retry_for_tid)
                found_first_call = self.__find_tid_with_retry(
                    open_search_helper, vpc, number_times_to_retry
                )
            else:
                raise LogEntryNotFound(
                    f"TID not found after {number_times_to_retry} retries"
                )

        return found_first_call

    def __find_logs_by_partial_message_search_with_retry(
        self, open_search_helper, search_text, number_times_to_retry=3
    ):
        found_logs = open_search_helper.search_message_by_partial_message_search(
            search_text
        )

        if len(found_logs) == 0:
            number_times_to_retry += 1
            if number_times_to_retry < 3:
                time.sleep(2)
                found_logs = self.__find_logs_by_partial_message_search_with_retry(
                    open_search_helper, search_text, number_times_to_retry
                )
            else:
                raise LogEntryNotFound(
                    f"Partial message [{search_text}] not found after {number_times_to_retry} retries"
                )
        return found_logs

    def __find_logs_by_tid_with_retry(
        self, open_search_helper, thread_id, number_times_to_retry=3
    ):
        found_logs = open_search_helper.search_message_by_tid(thread_id)

        if found_logs == "[tx: pl:]" or len(found_logs) == 0:
            number_times_to_retry += 1
            if number_times_to_retry < 3:
                time.sleep(10)
                found_logs = self.__find_logs_by_tid_with_retry(
                    open_search_helper, thread_id, number_times_to_retry
                )
            else:
                raise LogEntryNotFound(
                    f"No logs found via TID [{thread_id}] after {number_times_to_retry} retries"
                )

        return found_logs
