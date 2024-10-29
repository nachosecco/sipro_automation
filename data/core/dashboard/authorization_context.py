import logging

import requests

from core.dashboard.dashboard_api_exception import DashboardApiException
from core.util.app_utils import check_and_get_env


def get_authorization_context():
    app_url = check_and_get_env("DSE_DASHBOARD_API")
    username = check_and_get_env("DSE_API_USER")
    password = check_and_get_env("DSE_API_PWD")

    return AuthorizationContext(app_url, username, password)


class AuthorizationContext:
    """Class that has the context data to fetch a new token"""

    def __init__(self, dashboard_api, user, psw):
        self.dashboard_api = dashboard_api
        self.dashboard_user = user
        self.dashboard_psw = psw
        self.__fetch_token()

    def __fetch_token(self):

        url = self.dashboard_api + "/v2/auth"

        logging.debug("Fetching token for dashboard [%s]", url)

        data = {
            "username": self.dashboard_user,
            "password": self.dashboard_psw,
        }
        response = requests.request(method="POST", url=url, timeout=20, json=data)
        if not response.status_code == 202:
            raise DashboardApiException(
                f"error fetching token with status code {response.status_code} and message {response.text}"
            )

        dto = response.json()
        self.token = dto.get("authorization")

        self.company_id = dto.get("primaryCompanyId")

        logging.debug("The authorization token from the dashboard is [%s]", self.token)
