import inspect
import json

from jsonpath_ng import parse

from core.vastValidator import VastValidator


class RtbResponse:
    """Response validator for RTB requests"""

    def __init__(self, request_id, http_response):
        self.__response_headers = http_response.headers
        self.__response_status = http_response.status_code
        self.__request_id = str(request_id)
        self.__response_body = (
            json.loads(http_response.content)
            if len(http_response.content) != 0
            else None
        )
        caller_frame = inspect.stack()[1]
        key = caller_frame.function

    def is_ok(self) -> "RtbResponse":
        assert (
            self.__response_status == 200
        ), f"Status code expected to be 200 but was:{self.__response_status}"
        return self

    def is_empty(self) -> "RtbResponse":
        assert (
            self.__response_status == 204
        ), f"Status code expected to be 204 but was:{self.__response_status}"
        assert (
            self.__response_body is None
        ), f"Response payload was expected to be empty but was:{self.__response_body}"
        return self

    def is_server_error(self) -> "RtbResponse":
        assert (
            self.__response_status == 500
        ), f"Status code expected to be 500 but was:{self.__response_status}"
        return self

    def is_not_server_error(self) -> "RtbResponse":
        assert (
            self.__response_status != 500
        ), f"Status code expected not to be 500 but was:{self.__response_status}"
        return self

    def is_bad_request(self) -> "RtbResponse":
        assert (
            self.__response_status == 400
        ), f"Status code expected to be 400 but was:{self.__response_status}"
        return self

    def is_not_found(self) -> "RtbResponse":
        assert (
            self.__response_status == 404
        ), f"Status code expected to be 404 but was:{self.__response_status}"
        return self

    def has_error_message(self, expected) -> "RtbResponse":
        value = self.__response_body["error"]
        assert (
            value == expected
        ), f"error message differs from expected:{expected} vs {value}"
        return self

    def matches_request_transaction_id(self) -> "RtbResponse":
        if not self.__response_status == 200 and not self.__response_status == 204:
            value = self.__response_body["tid"]
            assert (
                value == self.__request_id
            ), f"tid value differs from expected: {self.__request_id} vs {value}"
        else:
            value = self.__response_body["id"]
            assert (
                value == self.__request_id
            ), f"id value differs from expected: {self.__request_id} vs {value}"

        return self

    def number_of_bids_is(self, expected: int, seat_bid=0) -> "RtbResponse":
        value = len(self.__response_body["seatbid"][seat_bid])
        assert (
            value == expected
        ), f"bids size differs from expected:{expected} vs {value}"
        return self

    def number_of_bidobjects_is(self, expected: int, seat_bid=0) -> "RtbResponse":
        value = len(self.__response_body["seatbid"][seat_bid]["bid"])
        assert (
            value == expected
        ), f"bid objects size differs from expected:{expected} vs {value}"
        return self

    def placement_uid_is(self, expected: str) -> "RtbResponse":
        value = self.__response_body["uid"]
        assert (
            value == expected
        ), f"placement id differs from expected:{expected} vs {value}"
        return self

    def price_is(self, expected: float, seat_bid=0, bid=0) -> "RtbResponse":
        value = self.__mandatory_extract_field_from_bid(seat_bid, bid, "price")
        assert value == expected, f"price differs from expected:{expected} vs {value}"
        return self

    def adomain_is(self, expected: list, seat_bid=0, bid=0) -> "RtbResponse":
        value = self.__mandatory_extract_field_from_bid(seat_bid, bid, "adomain")
        assert value == expected, f"adomain differs from expected:{expected} vs {value}"
        return self

    def cat_is(self, expected: list, seat_bid=0, bid=0) -> "RtbResponse":
        value = self.__mandatory_extract_field_from_bid(seat_bid, bid, "cat")
        assert value == expected, f"cat differs from expected:{expected} vs {value}"
        return self

    def deal_id_is(self, expected: str, seat_bid=0, bid=0):
        value = self.__optional_extract_field_from_bid(seat_bid, bid, "dealid")
        assert value == expected, f"dealid differs from expected:{expected} vs {value}"
        return self

    def validate_vast(self, seat_bid=0, bid=0) -> "VastValidator":
        value = self.__mandatory_extract_field_from_bid(seat_bid, bid, "adm")
        return VastValidator(value, self)

    def __mandatory_extract_field_from_bid(self, seat_bid: int, bid: int, field: str):
        expression = parse(f"$.seatbid[{seat_bid}].bid[{bid}].{field}")
        value = expression.find(self.__response_body)
        assert (
            value[0].value is not None
        ), f"Could not find {field} value for seatbid[{seat_bid}] bid[{bid}] in the response"
        return value[0].value

    def __optional_extract_field_from_bid(self, seat_bid: int, bid: int, field: str):
        expression = parse(f"$.seatbid[{seat_bid}].bid[{bid}].{field}")
        value = expression.find(self.__response_body)
        return value[0].value if len(value) > 0 else None
