import asyncio
import logging
from typing import Dict, List

import requests
from aiohttp import ClientSession

from core.configuration import Configuration

PLACEMENTS_RESOURCE_PATH = "/v2/manage/placements"

PLACEMENTS_ALIGNMENTS_RESOURCE_PATH = "/v2/manage/placements/alignments"

PUBLISHER_RESOURCE_PATH = "/v2/manage/publishers"
COMPANIES_PATH = "/v2/manage/companies"


DEFAULT_TIMEOUT_SECS = 5 * 60


class AuthorizationContext:
    def __init__(self, configuration):
        self.configuration = configuration
        self.__fetch_token()

    def __fetch_token(self):
        logger = logging.getLogger("resources")

        logger.debug("Fetching token for dashboard")

        if not self.configuration.dashboard_api:
            raise ValueError(
                "error the dashboard api , env [DSE_DASHBOARD_API] is not set"
            )

        if not self.configuration.api_user:
            raise ValueError(
                "error the user for dashboard api , env [DSE_API_USER] is not set"
            )

        if not self.configuration.api_pwd:
            raise ValueError(
                "error the password for dashboard api , env [DSE_API_PWD] is not set"
            )

        url = self.configuration.dashboard_api + "/v2/auth"
        data = {
            "username": self.configuration.api_user,
            "password": self.configuration.api_pwd,
        }
        response = requests.request(
            method="POST", url=url, timeout=DEFAULT_TIMEOUT_SECS, json=data
        )
        if not response.status_code == 202:
            raise RuntimeError(
                f"error fetching token with status code {response.status_code} and message {response.text}"
            )

        dto = response.json()
        self.token = dto.get("authorization")

        self.company_id = dto.get("primaryCompanyId")

        logger.debug(f"Token for dashboard is {self.token}")


class UtilResources:
    def __init__(self, configuration=Configuration()):
        self.configuration = configuration
        self.authorization_context = AuthorizationContext(configuration)
        self.supply = Supply(self)

    @staticmethod
    def collection_resources_to_dict_by_name(resources):
        return UtilResources.collection_resources_to_dict_by_key(resources, "name")

    @staticmethod
    def collection_resources_to_dict_by_guid(resources):
        return UtilResources.collection_resources_to_dict_by_key(resources, "guid")

    @staticmethod
    def collection_resources_to_dict_by_key(resources, field):
        logging.debug(f"converting {len(resources)} resources to dict by {field}")
        data = {}
        for resource in resources:
            data[resource.get(field)] = resource
        return data

    def get_resources(
        self, url_suffix: str, resource_name: str, additional_headers: Dict = None
    ):
        """
        Retrieve a resource from the Dashboard API

        url_suffix: Resource to be retrieved e.g. /v2/manage/rtb-bidders/1234
        resource_name: Name of the resource for logging purposes e.g. placement
        additional_headers: Optional Dict of headers to include in the request
        """
        url = f"{self.configuration.dashboard_api}{url_suffix}"
        headers = {"Authorization": self.authorization_context.token}
        if additional_headers is not None:
            headers.update(additional_headers)
        response = requests.request(
            method="GET", url=url, headers=headers, timeout=DEFAULT_TIMEOUT_SECS
        )
        if not response.status_code == 200:
            raise RuntimeError(
                f"error fetching {resource_name} index has the status code {response.status_code} "
                f"and message {response.text} "
            )

        data = response.json()

        return data

    def get_resources_async(
        self,
        url_suffix_list: List[str],
        additional_headers: Dict = None,
        max_concurrency=5,
    ):
        """
        Retrieve resources from the Dashboard API concurrently

        url_suffix_list: List of resources to be retrieved e.g. /v2/manage/rtb-bidders/1234
        additional_headers: Optional Dict of headers to include in the request
        max_concurrency: Number of concurrent requests to make. Default is 5
        """
        headers = {"Authorization": self.authorization_context.token}
        if additional_headers is not None:
            headers.update(additional_headers)

        return asyncio.run(
            self._fetch_resources_async(url_suffix_list, headers, max_concurrency)
        )

    async def _fetch_resources_async(
        self, url_suffix_list: List[str], headers: Dict = None, max_concurrency=5
    ):
        """
        Internal method for making concurrent requests to the Dashboard API
        This is a separate method so the external caller doesn't need to bother with calling an async method

        url_suffix_list: List of resources to be retrieved e.g. /v2/manage/rtb-bidders/
        headers: Optional Dict of headers to include in the request
        max_concurrency: Number of concurrent requests to make. Default is 5
        """
        semaphore = asyncio.Semaphore(max_concurrency)

        # Default timeout is 5 minutes
        async with ClientSession(
            base_url=self.configuration.dashboard_api,
            headers=headers,
            raise_for_status=True,
        ) as session:

            async def fetch_with_semaphore(url):
                async with semaphore:
                    async with session.get(url) as response:
                        return await response.json()

            tasks = [fetch_with_semaphore(url_suffix) for url_suffix in url_suffix_list]
            results = await asyncio.gather(*tasks)

            return results

    @staticmethod
    def resources_by_id(resources):
        data = {}
        for resource in resources:
            data[resource.get("id")] = resource
        return data


class Supply:
    def __init__(self, util_resources):
        self.util_resources = util_resources

    def find_placements_by_index(self, company_id=None):
        additional_headers = Company.get_company_override_header(company_id)
        return self.util_resources.get_resources(
            f"{PLACEMENTS_RESOURCE_PATH}", "placement", additional_headers
        )

    def find_all_alignment_placements(self, company_id=None):
        additional_headers = Company.get_company_override_header(company_id)
        return self.util_resources.get_resources(
            f"{PLACEMENTS_ALIGNMENTS_RESOURCE_PATH}", "alignments", additional_headers
        )

    def find_placement_by_id(self, id_placement):
        return self.util_resources.get_resources(
            f"{PLACEMENTS_RESOURCE_PATH}/{id_placement}", "placement"
        )

    def find_publisher_by_id(self, id_publisher):
        return self.util_resources.get_resources(
            f"{PUBLISHER_RESOURCE_PATH}/{id_publisher}", "publisher"
        )


class Company:
    def __init__(self, util_resources):
        self.util_resources = util_resources

    @staticmethod
    def get_company_override_header(company_id):
        additional_headers = {}
        if company_id is not None:
            additional_headers["X-COMPANY-OVERRIDE"] = str(company_id)
        return additional_headers

    def get_companies(self) -> Dict:
        return self.util_resources.collection_resources_to_dict_by_name(
            self.util_resources.get_resources(COMPANIES_PATH, "companies")
        )
