import logging

import requests
from requests import Response

from authorizationContext import AuthorizationContext


class ResourceUtil:
    def __init__(
        self,
        authorization_context: type(AuthorizationContext),
    ):
        self.authorization_context = authorization_context
        self.logger = logging.getLogger("extractor")

    def get_resource(self, resource_id: int, resource_name: str, api_url) -> Response:
        self.logger.debug(f"Fetching {resource_name} by id {resource_id}")

        response = requests.request(
            method="GET",
            url=api_url,
            headers={"Authorization": self.authorization_context.token},
        )
        if not (response.status_code == 200):
            raise Exception(
                f"error fetching {resource_name} by id {resource_id} has the status code {response.status_code} "
                f"and message {response.text} and the url {api_url}"
            )
        else:
            self.logger.info(f"Fetched {resource_name} by id {resource_id}")
            return response

    def get_resource_json(self, resource_id: int, resource_name: str, api_url):
        response = self.get_resource(resource_id, resource_name, api_url)
        return response.json()

    def get_resource_with_test_case_naming(
        self,
        resource_id: int,
        resource_name: str,
        api_url: str,
        case_name: str,
        name_key="name",
    ):
        data_resource = self.get_resource_json(resource_id, resource_name, api_url)

        data_resource[name_key] = case_name
        return data_resource

    def get_resource_index(self, resource_name: str, api_url: str):
        self.logger.debug(f"Fetching {resource_name} by index")

        response = requests.request(
            method="GET",
            url=api_url,
            headers={"Authorization": self.authorization_context.token},
        )
        if not (response.status_code == 200):
            raise Exception(
                f"error fetching {resource_name} index has the status code {response.status_code} "
                f"and message {response.text} "
            )
        else:
            self.logger.info(f"Fetched {resource_name}")
            return response.json()

    def resource_name_for_collection(
        self, case_name, resource_name, resource_collection, name_key="name"
    ):
        """
        Each resource we create for a given test case will share a name with the test case name.
        For instances where we need to create multiple resources for a test,
        such as multiple bidders for a deal, we label them sequentially as "Case Name 1, Case Name 2, etc."
        """

        if len(resource_collection) > 1:
            self.logger.debug(f"assign {resource_name} name to case plus #")
            resource_number = 1
            for resource in resource_collection:
                resource[name_key] = f"{case_name} [{resource_number}]"
                resource_number = resource_number + 1
        elif len(resource_collection) == 1:
            resource_collection[0][name_key] = case_name
        return resource_collection
