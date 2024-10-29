import re
import logging
from core.constants import ComparisonType as CT
from core.constants import UNKNOWN, REPLACE


def compare_values(
    actual_value: str, expected_value: str, property_name: str, comparison_type: CT
):
    result = False
    if comparison_type == CT.Equality:
        result = expected_value == actual_value
    elif comparison_type == CT.Startswith:
        result = actual_value.startswith(expected_value)
    elif comparison_type == CT.Endswith:
        result = actual_value.endswith(expected_value)
    elif comparison_type == CT.Contains:
        result = expected_value in actual_value
    elif comparison_type == CT.Pattern:
        pattern = re.compile(expected_value)
        result = pattern.search(actual_value) is not None
    elif comparison_type == CT.NotEmpty:
        result = len(actual_value) > 0

    if result:
        logging.info("Value for '%s' property  matched", property_name)
    else:
        logging.error(
            "Expected value for property '%s' was '%s', but actual value is '%s'",
            property_name,
            expected_value,
            actual_value,
        )
    assert result


def get_split_char(value_log):
    next_line_pos = value_log.find("\n")
    quotes_pos = value_log.find('"')
    return '"' if next_line_pos == -1 or quotes_pos < next_line_pos else "\n"


def get_split_char_without_quotes(value_log):
    next_line_pos = value_log.find("\n")
    space_pos = value_log.find(" ")
    return " " if next_line_pos == -1 or space_pos < next_line_pos else "\n"


def compare_result(
    token: str,
    expected_value,
    log: str,
    comparison_type: CT = CT.Equality,
):
    if expected_value in ["", 0, UNKNOWN, REPLACE]:
        return True
    actual_value = parse_token(token, log)
    log_name = token.split(":")[0]

    compare_values(actual_value, expected_value, log_name, comparison_type)


def parse_token(token: str, log: str):
    if log.find(token) != -1:
        value_log = log.split(token, 1)[1]
        split_char = get_split_char(value_log)
        return value_log.split(split_char, 1)[0]
    return ""


def compare_result_without_quotes(
    token: str,
    expected_value,
    log: str,
    comparison_type: CT = CT.Equality,
):
    if expected_value in ["", 0, UNKNOWN, REPLACE]:
        return True
    actual_value = parse_token_without_quotes(token, log)
    log_name = token.split(":")[0]

    compare_values(actual_value, expected_value, log_name, comparison_type)


def parse_token_without_quotes(token, log):
    if log.find(token) != -1:
        value_log = log.split(token, 1)[1]
        split_char = get_split_char_without_quotes(value_log)
        return value_log.split(split_char, 1)[0]
    return ""
