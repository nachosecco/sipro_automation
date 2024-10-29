from core.vastXMLAssertor import VastResultAssertor


class RouterResult:
    def __init__(self, vast_result_asserter: VastResultAssertor, logs=None):
        if logs is None:
            logs = []
        self.vast_result_assert = vast_result_asserter
        self.logs = logs
