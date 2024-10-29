import logging


class IVTRequest:
    def __init__(self, input_log_line=None):
        self.user_agent = ""
        self.ip = ""
        self.device_id = ""
        self.threshold = ""
        self.input_log_line_found = False

        if input_log_line is not None:
            self.input_log_line_found = True
            self.__parse_input_log_line(input_log_line)

    def __repr__(self):
        return (
            f"User_Agent: {self.user_agent}, "
            f"IP: {self.ip}, "
            f"Device_Id: {self.device_id}, "
            f"Threshold: {self.threshold}, "
            f"Input Log Line Found: {self.input_log_line_found}"
        )

    def __parse_input_log_line(self, input_log_line):
        user_agent_start = input_log_line.find("userAgent=")
        ip_start = input_log_line.find("ip=", user_agent_start)
        device_id_start = input_log_line.find("deviceId=", ip_start)
        threshold_start = input_log_line.find("threshold=", device_id_start)
        ivt_response_start = input_log_line.find("- IVT response is", threshold_start)

        if (
            user_agent_start == -1
            or ip_start == -1
            or device_id_start == -1
            or threshold_start == -1
            or ivt_response_start == -1
        ):
            raise ValueError(
                f"Failed to find a token when parsing inputLogLine for IVTRequest: "
                f"{input_log_line=}, {user_agent_start=}, {ip_start=}, {device_id_start=}, {threshold_start=}, {ivt_response_start=}"
            )

        user_agent_end = ip_start - 2
        ip_end = device_id_start - 2
        device_id_end = threshold_start - 2
        threshold_end = ivt_response_start - 1

        self.user_agent = input_log_line[user_agent_start + 10 : user_agent_end]
        self.ip = input_log_line[ip_start + 3 : ip_end]
        self.device_id = input_log_line[device_id_start + 9 : device_id_end]
        self.threshold = input_log_line[threshold_start + 10 : threshold_end]


class IVTResponseMaxProbability:
    def __init__(self, max_probability_value=None):
        self.is_null = False
        self.probability = ""
        self.category = ""

        if max_probability_value is not None:
            self.__parse_max_probability_value(max_probability_value)

    def __repr__(self):
        return (
            f"IsNull: {self.is_null}, "
            f"Probability: {self.probability}, "
            f"Category: {self.category}"
        )

    def __parse_max_probability_value(self, max_probability_value):
        if max_probability_value == "null":
            self.is_null = True
        else:
            probability_start = max_probability_value.find("probability=")
            category_start = max_probability_value.find("category=")

            if probability_start == -1 or category_start == -1:
                raise ValueError(
                    f"Failed to find a token when parsing maxProbabilityValue for IVTResponseMaxProbability: "
                    f"{max_probability_value=}, {probability_start=}, {category_start=}"
                )

            probability_end = category_start - 2
            category_end = len(max_probability_value) - 1

            self.probability = max_probability_value[
                probability_start + 12 : probability_end
            ]
            self.category = max_probability_value[category_start + 9 : category_end]


class IVTResponseCheck:
    def __init__(self, check_value=None):
        self.probability = ""
        self.result = ""
        self.detail = ""
        self.category = ""

        if check_value is not None:
            self.__parse_check_value(check_value)

    def __repr__(self):
        return (
            f"Probability: {self.probability}, "
            f"Result: {self.result}, "
            f"Detail: {self.detail}, "
            f"Category: {self.category}"
        )

    def __parse_check_value(self, check_value):
        probability_start = check_value.find("probability=")
        result_start = check_value.find("result=", probability_start)
        detail_start = check_value.find("detail=", result_start)
        category_start = check_value.find("category=", detail_start)

        if (
            probability_start == -1
            or result_start == -1
            or detail_start == -1
            or category_start == -1
        ):
            raise ValueError(
                f"Failed to find a token when parsing checkValue for IVTResponseCheck: "
                f"{check_value}, {probability_start}, {result_start}, {detail_start}, {category_start}"
            )

        probability_end = result_start - 2
        result_end = detail_start - 2
        detail_end = category_start - 2
        category_end = len(check_value) - 1

        self.probability = check_value[probability_start + 12 : probability_end]
        self.result = check_value[result_start + 7 : result_end]
        self.detail = check_value[detail_start + 7 : detail_end]
        self.category = check_value[category_start + 9 : category_end]


class IVTResponseChecks:
    def __init__(self, checks_value=None):
        self.device_id = IVTResponseCheck()
        self.ip_v4 = IVTResponseCheck()
        self.ip_v6 = IVTResponseCheck()
        self.user_agent = IVTResponseCheck()

        if checks_value is not None:
            self.__parse_checks_value(checks_value)

    def __repr__(self):
        return (
            f"DeviceId: ({self.device_id}), "
            f"IPV4: ({self.ip_v4}), "
            f"IPV6: ({self.ip_v6}), "
            f"User Agent: ({self.user_agent})"
        )

    def __parse_checks_value(self, checks_value):
        device_id_start = checks_value.find("deviceId=")
        if device_id_start != -1:
            device_id_end = checks_value.find(")", device_id_start)
            self.device_id = IVTResponseCheck(
                checks_value[device_id_start + 9 : device_id_end + 1]
            )

        ip_v4_start = checks_value.find("ipV4=")
        if ip_v4_start != -1:
            ip_v4_end = checks_value.find(")", ip_v4_start)
            self.ip_v4 = IVTResponseCheck(checks_value[ip_v4_start + 5 : ip_v4_end + 1])

        ip_v6_start = checks_value.find("ipV6=")
        if ip_v6_start != -1:
            ip_v6_end = checks_value.find(")", ip_v6_start)
            self.ip_v6 = IVTResponseCheck(checks_value[ip_v6_start + 5 : ip_v6_end + 1])

        user_agent_start = checks_value.find("userAgent=")
        if user_agent_start != -1:
            user_agent_end = checks_value.find(")", user_agent_start)
            self.user_agent = IVTResponseCheck(
                checks_value[user_agent_start + 10 : user_agent_end + 1]
            )


class IVTResponse:
    def __init__(self, input_log_line=None, did_not_pass_log_line=None):
        self.max_probability = IVTResponseMaxProbability()
        self.is_partial = ""
        self.is_passed = ""
        self.checks = IVTResponseChecks()
        self.error = ""
        self.did_not_pass_category = ""
        self.did_not_pass_probability = ""

        if input_log_line is not None:
            self.__parse_input_log_line(input_log_line)
        if did_not_pass_log_line is not None:
            self.__parse_did_not_pass_log_line(did_not_pass_log_line)

    def __repr__(self):
        return (
            f"Max Probability: ({self.max_probability}), "
            f"Partial: {self.is_partial}, "
            f"Passed: {self.is_passed}, "
            f"Checks: ({self.checks}), "
            f"Error: {self.error}, "
            f"DidNotPassCategory: {self.did_not_pass_category}, "
            f"DidNotPassProbability: {self.did_not_pass_probability}"
        )

    def __parse_input_log_line(self, input_log_line):
        max_probability_start = input_log_line.find("maxProbability=")
        partial_start = input_log_line.find("partial=", max_probability_start)
        pass_start = input_log_line.find("pass=", partial_start)
        checks_start = input_log_line.find("checks=", pass_start)
        error_start = input_log_line.find("error=", checks_start)

        if (
            max_probability_start == -1
            or partial_start == -1
            or pass_start == -1
            or checks_start == -1
            or error_start == -1
        ):
            raise ValueError(
                f"Failed to find a token when parsing inputLogLine for IVTResponse: "
                f"{input_log_line}, {max_probability_start}, {partial_start}, {pass_start}, {checks_start}, {error_start}"
            )

        max_probability_end = partial_start - 2
        partial_end = pass_start - 2
        pass_end = checks_start - 2
        checks_end = error_start - 2
        error_end = len(input_log_line) - 1

        max_probability_value = input_log_line[
            max_probability_start + 15 : max_probability_end
        ]
        self.max_probability = IVTResponseMaxProbability(max_probability_value)

        self.is_partial = input_log_line[partial_start + 8 : partial_end]
        self.is_passed = input_log_line[pass_start + 5 : pass_end]

        checks_value = input_log_line[checks_start + 7 : checks_end]
        self.checks = IVTResponseChecks(checks_value)

        self.error = input_log_line[error_start + 6 : error_end]

    def __parse_did_not_pass_log_line(self, did_not_pass_log_line):
        category_start = did_not_pass_log_line.find("category=")
        probability_start = did_not_pass_log_line.find("probability=", category_start)
        for_input_start = did_not_pass_log_line.find("for input:", probability_start)

        if category_start == -1 or probability_start == -1 or for_input_start == -1:
            raise ValueError(
                f"Failed to find a token when parsing didNoPassLogLine for IVTResponse: "
                f"{did_not_pass_log_line} {category_start}, {probability_start}, {for_input_start}"
            )

        category_end = probability_start - 2
        probability_end = for_input_start - 1

        self.did_not_pass_category = did_not_pass_log_line[
            category_start + 9 : category_end
        ]
        self.did_not_pass_probability = did_not_pass_log_line[
            probability_start + 12 : probability_end
        ]


class IVT:
    def __init__(self, delivery_logs):
        (
            input_log_line,
            did_not_pass_log_line,
            filter_reason_log_line,
        ) = self.__find_ivt_logs(delivery_logs)
        logging.debug(f"InputLogLine: {input_log_line}")
        logging.debug(f"DidNotPassLogLine: {did_not_pass_log_line}")
        logging.debug(f"FilterReasonLogLine: {filter_reason_log_line}")

        self.request = IVTRequest(input_log_line)
        logging.debug(f"Request: {self.request}")

        self.response = IVTResponse(input_log_line, did_not_pass_log_line)
        logging.debug(f"Response: {self.response}")

        self.filter_reason = self.__parse_filter_reason(filter_reason_log_line)
        logging.debug(f"FilterReason: {self.filter_reason}")

    def __repr__(self):
        return (
            f"IVT Request: {self.request}, "
            f"IVT Response: {self.response}, "
            f"Filter Reason: {self.filter_reason}"
        )

    def __find_ivt_logs(self, delivery_logs):
        input_log_line = None
        did_not_pass_log_line = None
        filter_reason_log_line = None

        for log in delivery_logs:
            if log.startswith("for input:"):
                input_log_line = log
            elif log.startswith("IVT check did not pass:"):
                did_not_pass_log_line = log
            elif log.startswith("Check IVTCheck returned: "):
                filter_reason_log_line = log

            if input_log_line and did_not_pass_log_line and filter_reason_log_line:
                break

        return (input_log_line, did_not_pass_log_line, filter_reason_log_line)

    def __parse_filter_reason(self, filter_reason_log_line):
        if filter_reason_log_line is None:
            return "No Filter Reason Found"

        # Skip the leading 25 chars of 'Check IVTCheck returned: '
        return filter_reason_log_line[25:].strip()
