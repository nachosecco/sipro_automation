from datetime import datetime
import logging
import os
from core.logReaderOpenSearch import LogReaderFromOpenSearch
from core.vpc import VPC
from core.configuration import Configuration


# Class to read a Logger from the current host
class LogReaderLocal:
    def __init__(self, vpc: VPC):
        self.tid = None
        self.vpc = vpc

    def read_delivery(self, vpc, values_to_find_in_log, retry=True, retry_count=0):
        path_to_script = os.getenv(
            "READ_LOG_PATH_DELIVERY", "CHANGE_ENV_VAR_READ_LOG_PATH_DELIVERY"
        )
        return self.__read(path_to_script, values_to_find_in_log)

    def read_logs_events(self, contains_to_test, retry=True, retry_count=0):
        path_to_script = os.getenv(
            "READ_LOG_PATH_EVENTS", "CHANGE_ENV_VAR_READ_LOG_PATH_EVENTS"
        )
        return self.__read(path_to_script, contains_to_test)

    @staticmethod
    def __read(path_to_script, contains):
        log_lines = int(os.getenv("READ_LOG_LINES_TO_READ", "2000"))
        with open(path_to_script) as log:
            for line in log.readlines()[-log_lines:]:
                for contain in contains:
                    if contain in line:
                        contains.remove(contain)
                        break
        if not len(contains) == 0:
            logging.error("Assertions Not found in logs " + str(contains))
        return len(contains) == 0

    @staticmethod
    def handle_multi_lines(log_fh):
        lines = []
        for line in log_fh:
            if "][tx:" in line:
                lines.append(line)
            else:
                if len(lines) - 1 >= 0:
                    lines[len(lines) - 1] += line
                else:
                    lines.append(line)
        return lines

    def __read_all_lines(self, path_to_log, tid):
        max_number_log_lines_to_read = int(os.getenv("READ_LOG_LINES_TO_READ", "2000"))
        contains = []
        with open(path_to_log) as log:
            logs = self.handle_multi_lines(
                log.readlines()[-max_number_log_lines_to_read:]
            )
            for line in logs:
                if tid in line:
                    contains.append(line)

        if not len(contains) == 0:
            if len(contains) < 10:
                logging.error("Assertions Not found in logs " + str(contains))
            else:
                logging.error(f"Assertions Not found in logs with the tid [{tid}]")
        return contains

    def find_logs_delivery(self, vpc):
        path_to_script = os.getenv(
            "READ_LOG_PATH_DELIVERY", "CHANGE_ENV_VAR_READ_LOG_PATH_DELIVERY"
        )
        lines = self.__read_all_lines(path_to_script, self.vpc._automationFramework)
        start = lines[0].find("[tx:")
        end = lines[0].find(" pl:")
        logging.info(
            "tid:"
            + lines[0][start:end]
            + " automationId:"
            + self.vpc._automationFramework
        )
        return self.__read_all_lines(path_to_script, lines[0][start:end])

    def set_tid(self, tid: str):
        self.tid = tid

    def find_logs_events(self):
        path_to_script = os.getenv(
            "READ_LOG_PATH_EVENTS", "CHANGE_ENV_VAR_READ_LOG_PATH_EVENTS"
        )
        lines = self.__read_all_lines(path_to_script, self.vpc._automationFramework)
        if len(lines) == 0:
            return []

        start = lines[0].find("[tx:")
        end = lines[0].find(" pl:")
        logging.info(
            "tid:"
            + lines[0][start:end]
            + lines[0][start:end]
            + " automationId:"
            + self.vpc._automationFramework
        )
        return self.__read_all_lines(path_to_script, lines[0][start:end])


# This is a wrapper class that choose the implementation of log reader that is going to be used
class LogReader:
    def __init__(self, vpc: VPC, config_override: Configuration = None):
        self.vpc = vpc
        self.configOverride = config_override
        self.reader = self.__log_reader_strategy()
        self.tid = None

    def __log_reader_strategy(self):
        strategy = os.getenv("READ_LOG_STRATEGY", "CHANGE_ENV_VAR_READ_LOG_STRATEGY")
        if strategy == "CHANGE_ENV_VAR_READ_LOG_STRATEGY":
            raise Exception(
                'READ_LOG_STRATEGY is a variable that is required, valid values are ("LOCAL","OPEN_SEARCH"'
            )

        if strategy == "LOCAL":
            return LogReaderLocal(self.vpc)

        if strategy == "OPEN_SEARCH":
            return LogReaderFromOpenSearch(
                self.vpc._automationFramework, self.configOverride
            )

        raise Exception(
            'Invalid READ_LOG_STRATEGY, valid values are ("LOCAL","OPEN_SEARCH"'
        )

    # Would return a true if the contains is in the log
    def read_delivery(self, values_to_find_in_log, retry=True, retry_count=0):
        retry_max_time_delivery = int(os.getenv("DF_CONFIG_RETRY_LOG_DELIVERY", "2"))

        value_was_found = self.reader.read_delivery(self.vpc, values_to_find_in_log)
        if not value_was_found and retry and retry_count < retry_max_time_delivery:
            logging.info(
                "Retry find in the log, for values : "
                + str(values_to_find_in_log)
                + " retry_count is "
                + str(retry_count)
            )
            retry_count += 1
            value_was_found = self.read_delivery(
                values_to_find_in_log, True, retry_count
            )
        return value_was_found

    # Would return a true if the contains is in the log
    def read_events(self, contains_to_test, event_logs):
        return self.reader.read_events(contains_to_test, event_logs)

    def find_logs_delivery(self):
        return self.reader.find_logs_delivery(self.vpc)

    def find_logs_events(self):
        return self.reader.find_logs_events()

    def find_logs_quartzalignment(self, text_to_search):
        return self.reader.find_logs_quartzalignment(text_to_search)

    def set_tid(self, tid: str):
        self.tid = tid
        self.reader.set_tid(tid)


class SavedLogReader:
    def __init__(self, app: str, directory: str, logs):
        currentTime = datetime.now().strftime("%Y%m%d.%H%M%S")
        self.path = directory + app + "_" + currentTime + ".log"
        self.logs = logs
        logging.info("Saving the logs in the path:" + self.path)
        with open(self.path, "w") as f:
            f.write(str(self.logs))
