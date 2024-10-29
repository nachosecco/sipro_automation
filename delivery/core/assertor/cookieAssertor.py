import logging
from core.constants import ComparisonType
from core.dto.cookie import UserCookie
from core.utils.stringUtils import subStringBetween
from core.utils.validationUtils import (
    parse_token,
    compare_result_without_quotes,
    parse_token_without_quotes,
)


class CookieAssertor:
    def __init__(self, logs):
        self.logs = logs
        self.cookie_log = None

    def parse_cookie_log(self, startsWith: str, endsWith: str):
        found = False
        for log in self.logs:
            self.cookie_log = subStringBetween(log, startsWith, endsWith)
            if self.cookie_log == "":
                continue
            else:
                found = True
                break
        assert found
        return self

    def get_value(self, key: str, withQuotes=False):
        return (
            parse_token(key, self.cookie_log)
            if withQuotes
            else parse_token_without_quotes(key, self.cookie_log)
        )

    def assert_expected_user_cookies_in_logs(self, expected_cookie: UserCookie):
        log = self.cookie_log
        if log is not None:
            compare_result_without_quotes(
                "sessionUUID=",
                expected_cookie.sessionUUID,
                log,
                ComparisonType.Startswith,
            )

    def get_device_id(self):
        return self.get_value("id=").rstrip(",")
