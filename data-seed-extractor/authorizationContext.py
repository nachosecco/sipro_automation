import requests
import logging


class AuthorizationContext:
    def __init__(self, configuration):
        self.configuration = configuration
        self.__fetch_token()

    def __fetch_token(self):
        logger = logging.getLogger("extractor")

        logger.debug("Fetching token for dashboard")

        if (
            self.configuration.dashboard_api == ""
            or self.configuration.dashboard_api is None
        ):
            raise Exception(
                f"error the dashboard api , env [DSE_DASHBOARD_API] is not set "
            )

        url = self.configuration.dashboard_api + "/v2/auth"
        data = {
            "username": self.configuration.api_user,
            "password": self.configuration.api_pwd,
        }
        response = requests.request(method="POST", url=url, json=data)
        if not (response.status_code == 202):
            raise Exception(
                f"error fetching token with status code {response.status_code} and message {response.text}"
            )

        dto = response.json()
        self.token = dto.get("authorization")

        self.company_id = dto.get("primaryCompanyId")

        logger.debug(f"Token for dashboard is {self.token}")
