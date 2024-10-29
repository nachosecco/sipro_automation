import logging

import requests

from core.dashboard.authorization_context import AuthorizationContext
from core.dashboard.dashboard_api_exception import DashboardApiException


class ResourceUtil:
    """Util class to use dashboard api methods in a generic way"""

    def __init__(self, authorization_context: type(AuthorizationContext)):
        self.authorization_context = authorization_context
        self.dashboard_api = authorization_context.dashboard_api

    def get_resource_index(self, resource_url: str, resource_name: str):
        api_url = self.dashboard_api + resource_url
        logging.debug("Fetching [%s] by index in path [%s]", resource_name, api_url)

        response = requests.request(
            method="GET",
            url=api_url,
            timeout=180,
            headers={"Authorization": self.authorization_context.token},
        )
        if not response.status_code == 200:
            raise DashboardApiException(
                f"error fetching {resource_name} index has the status code {response.status_code} "
                f"and message {response.text} "
            )

        return response.json()

    def delete_resource(self, resource_url, resource_name):
        api_url = self.dashboard_api + resource_url
        logging.debug("Deleting [%s] in path [%s]", resource_name, api_url)

        response = requests.request(
            method="DELETE",
            url=api_url,
            timeout=120,
            headers={"Authorization": self.authorization_context.token},
        )
        if response.status_code not in (200, 204):
            logging.error(
                "there was error with deleting [%s] the  error message [%s]",
                resource_name,
                response.text,
            )
            raise DashboardApiException(
                f"error deleting {resource_name} have the status code {response.status_code} "
                f"and message {response.text}"
            )
