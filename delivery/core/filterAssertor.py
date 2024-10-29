from core.vpc import VPC
from core.enums.filterReason import FilterReason
import logging


class FilterAssertor:
    """This class represent the class that would assert the vast against the values of a AdPod"""

    def __init__(self, logs, vpc: VPC, filter_reason: FilterReason):
        self.logs = logs
        self.filter_reason = filter_reason
        self.vpc = vpc

    def __find_log_entry(self):
        for log in self.logs:
            filter_reason_log = self.filter_reason.get_formatted_string(self.vpc)
            if log.find(filter_reason_log) != -1:
                return log

        return ""

    def validate_reason(self):
        assert self.is_filter_reason_found()

    def is_filter_reason_found(self):
        assert_result = self.__find_log_entry()
        if not assert_result:
            logging.error(
                "The expected Filter[%s] was not found with the message [%s]",
                self.filter_reason,
                self.filter_reason.get_formatted_string(self.vpc),
            )
        return assert_result
