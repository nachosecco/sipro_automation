class ResponseHeadersValidator:
    def __init__(self, response_headers):
        self.response_headers = response_headers

    def assert_header_nonempty(self, header_name):
        expected_header = self.response_headers.get(header_name, None)
        assert expected_header is not None
        assert expected_header is not ""

    def assert_header_value(self, header_name, expected_value):
        expected_header = self.response_headers.get(header_name, None)
        assert expected_value in expected_header

    def assert_header_not_present(self, header_name):
        assert self.response_headers.get(header_name, None) is None
