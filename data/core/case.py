from core.asserter.athena.athena_asserter import AthenaAsserter
from core.asserter.druid.druid_asserter import DruidAsserter
from core.configuration import Configuration
from core.dashboard.authorization_context import (
    get_authorization_context,
)
from core.delivery_controller import DeliveryControllers, CommonController
from core.delivery_parameters import DeliveryParameters
from core.event_coordinator import EventCoordinator
from core.util.data_csv_util import load_case_context


class Case:
    """Representation of case to test"""

    def __init__(self, name, configuration=Configuration()):
        self.name = name
        self.delivery_parameters = DeliveryParameters()
        self.configuration = configuration
        self.case_name_execution = name + "_" + self.configuration.execution_id
        self.context = load_case_context(
            self.case_name_execution,
            self.configuration.csv_path_file,
        )
        self.delivery_parameters.uid = self.context.placement_guid
        self.__auth_context = None

    def get_authorization_context(self):
        if self.__auth_context is None:
            self.__auth_context = get_authorization_context()

        return self.__auth_context

    def delivery_controller(self):
        return DeliveryControllers(self)

    def event_coordinator(self, controller: CommonController):
        return EventCoordinator(self, controller)

    def assert_in_druid(self):
        return DruidAsserter(self)

    def assert_in_athena(self):
        return AthenaAsserter(self)
