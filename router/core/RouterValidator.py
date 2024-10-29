import logging
import os
import uuid
from xml.etree import ElementTree as elementTree

import requests

from core import Routers
from core.RouterLogReader import LogReader
from core.RouterResult import RouterResult
from core.RoutersConstants import (
    AF_ID_INVENTORY_ROUTERS,
    AF_ID_INVENTORY_ROUTERS_INDIVIDUAL,
)
from core.configuration import Configuration
from core.vastClientSideValidator import VastClientSideValidator
from core.vastXMLAssertor import VastResultAssertor
from core.vpc import VPC


class ValidatorConfig:
    def __init__(
        self,
        number_of_times_to_execute=1,
        approximation_error=1,
        expected_status_code=200,
    ):
        self.expected_status_code = expected_status_code
        self.number_of_times_to_execute = number_of_times_to_execute
        self.approximation_error = approximation_error

        if expected_status_code != 200 and number_of_times_to_execute > 1:
            raise ValueError(
                "When status is not 200 and the number times of execution can only be 1"
            )


class Asserter:
    def __init__(self, config: ValidatorConfig, inventory_router_results=None):
        if inventory_router_results is None:
            inventory_router_results = []
        self.__demand_sources = {}
        self.__config = config
        self.inventory_router_results = inventory_router_results
        self._fill_demand_sources()

    def assert_demand_sources(self, expected_demand_sources):
        actual_demand_sources = self.__demand_sources
        config = self.__config
        for key in expected_demand_sources:
            if key in actual_demand_sources:
                actual_demand_source = actual_demand_sources[key]
                expected_demand_source = expected_demand_sources[key]
                actual_allocation = (
                    actual_demand_source / config.number_of_times_to_execute
                )
                expected_allocation = (
                    expected_demand_source + config.approximation_error
                )

                if actual_allocation > expected_allocation:
                    logging.error(
                        f"The expected demand source [{key}] has a executed a allocation [{actual_allocation}]"
                        f"  higher than expected [{expected_allocation}]"
                    )
                    assert False

            else:
                logging.error(
                    f"The expected demand source [{key}] is not found "
                    f"in the executed demand sources [{actual_demand_sources}]"
                )
                assert False

    def _fill_demand_sources(self):
        for result in self.inventory_router_results:

            for log in result.logs:
                if "selected the demand source " in log:
                    # The number 83, represent in the log, the start of the guid, in the log
                    demand_source_tmp = log[83:]

                    demand_source_selected = demand_source_tmp[
                        : demand_source_tmp.find("]")
                    ]

                    self.__demand_sources[demand_source_selected] = (
                        self.__demand_sources.get(demand_source_selected, 0) + 1
                    )
                    break

        logging.info("demandSources executed ->" + str(self.__demand_sources))


class Validator:
    def __init__(self):
        self.inventory_routers_executions_results = []

    def test(
        self,
        router: Routers,
        config=ValidatorConfig(),
        external_config=Configuration(),
    ) -> Asserter:

        routers_id_test = str(uuid.uuid4())

        logging.info(
            f"Inventory Router is going to be executed [{config.number_of_times_to_execute} "
            f"times with routers_id_test [{routers_id_test}]"
        )

        router_url = router.url() + f"{AF_ID_INVENTORY_ROUTERS}={routers_id_test}"
        logging.info("Testing the inventory routers path url => " + router_url)

        directory_case = "build/case" + routers_id_test + "/"
        os.makedirs(directory_case, exist_ok=True)
        inventory_routers_executions_results = self.inventory_routers_executions_results
        for executionNumber in range(config.number_of_times_to_execute):
            automation_framework = str(uuid.uuid4())
            url = (
                router_url
                + f"&{AF_ID_INVENTORY_ROUTERS_INDIVIDUAL}={automation_framework}"
                + f"&executionNumber={str(executionNumber)}"
            )
            result_execution = self.__execute_for_one(
                config,
                url,
                executionNumber,
                directory_case,
                automation_framework,
                router,
                external_config,
            )
            inventory_routers_executions_results.append(result_execution)

        return Asserter(config, inventory_routers_executions_results)

    @staticmethod
    def __execute_for_one(
        config,
        url,
        execution_number,
        directory_case,
        automation_framework,
        router,
        external_config,
    ):

        vast_response = requests.get(url)
        headers = vast_response.headers

        # always check that the status code is the expected one.
        if not vast_response.status_code == config.expected_status_code:
            logging.warning(
                f"The status code of the request was {vast_response.status_code}"
            )

        assert vast_response.status_code == config.expected_status_code

        directory_path_vast_response = (
            f"{directory_case}ex_number_{execution_number}_id_{automation_framework}/"
        )
        os.makedirs(directory_path_vast_response, exist_ok=True)

        with open(directory_path_vast_response + "vast_response.xml", "w") as f:
            f.write(vast_response.text)
        vast_parse_response = elementTree.parse(
            source=directory_path_vast_response + "vast_response.xml"
        )

        # always check that is a valid vast
        result_client = VastClientSideValidator(
            vast_response.text, automation_framework
        ).execute()
        assert result_client.validVast

        # Creating a copy of vpc, with the values from inventory routers
        vpc = VPC()
        fields = vars(router)
        for v in fields:
            if not v.startswith("_"):
                setattr(vpc, v, fields[v])

        # Using the same id, because it could work to delivery too
        vpc._automationFramework = automation_framework
        log_reader = LogReader(automation_framework, external_config)
        logs = log_reader.find_logs_inventory_routers()

        vast_result = VastResultAssertor(
            vast_parse_response,
            vast_response.status_code,
            vpc,
            directory_path_vast_response,
            headers,
            None,
        )

        return RouterResult(vast_result, logs)
