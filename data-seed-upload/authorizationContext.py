import requests
import logging


class AuthorizationContext:
    def __init__(self, configuration):
        self.configuration = configuration
        self.__fetch_token()

    def __fetch_token(self):
        logger = logging.getLogger("extractor")

        logger.debug("Fetching token for dashboard")

        url = self.configuration.dashboard_api + "/v2/auth"
        if len(self.configuration.api_user) == 0:
            logger.error("The variable DSE_DASHBOARD_API as not value")

        if len(self.configuration.api_pwd) == 0:
            logger.error("The variable DSE_API_PWD as not value")

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

        logger.debug("Found token for dashboard is " + self.token)
