import json
import logging

from core.configuration import Configuration
from core.utilResources import UtilResources, Company

RTB_BIDDERS_PATH = "/v2/manage/rtb-bidders"
NUM_CONCURRENT_REQUESTS = 10


class BidderDataFile:
    """Class to generate a file with all bidder data"""

    def __init__(self, configuration=Configuration()):
        self.__setup_logger()
        self.util_resources = UtilResources()
        self.company_cache = Company(self.util_resources).get_companies()
        self.configuration = configuration

    def __setup_logger(self):
        logging.basicConfig(format="%(asctime)s [%(levelname)8.8s] %(message)s")

        logger = logging.getLogger("csv")
        logger.setLevel(logging.DEBUG)

        self.logger = logger

    def __company_id_from_name(self, company_name):
        company_id = self.company_cache.get(company_name, {}).get("id", None)
        if not company_id:
            raise ValueError(f"Company with name {company_name} not found")
        return company_id

    def __company_name_from_id(self, company_id):
        for company_name, company in self.company_cache.items():
            if company["id"] == company_id:
                return company_name
        raise ValueError(f"Company with id {company_id} not found")

    def __fetch_and_write_bidders_to_file(self, company_names):
        """
        Retrieve all Bidders associated with the given company id
        Write the details of each Bidder as a JSON object in the output file. One Bidder object per line.
        """
        bidder_data_file_path = (
            f"data/bidder-data-file-env-{self.configuration.environment}.dat"
        )
        self.logger.info(f"Generating/Updating file {bidder_data_file_path}")
        final_bidder_data = []
        for company_name in company_names:
            self.logger.info(f"Fetching bidders for company {company_name}")
            company_id = self.__company_id_from_name(company_name)
            additional_headers = Company.get_company_override_header(company_id)
            list_of_bidders = self.util_resources.get_resources(
                RTB_BIDDERS_PATH, "rtb-bidders", additional_headers
            )
            self.logger.info(f"Found {len(list_of_bidders)} bidders")
            bidder_url_suffixes = []

            for bidder in list_of_bidders:
                bidder_id = bidder["id"]
                bidder_url_suffixes.append(f"{RTB_BIDDERS_PATH}/{bidder_id}")

            list_of_bidder_details = self.util_resources.get_resources_async(
                bidder_url_suffixes,
                additional_headers,
                max_concurrency=NUM_CONCURRENT_REQUESTS,
            )
            self.logger.info(f"Found {len(list_of_bidder_details)} bidder details")

            for bidder in list_of_bidder_details:
                bidder["company_id"] = company_id
                bidder["company_name"] = company_name
                final_bidder_data.append(bidder)

        with open(bidder_data_file_path, "w") as bidder_data_file:
            for bidder in final_bidder_data:
                bidder_data_file.write(f"{json.dumps(bidder)}\n")

    def generate(self):
        """
        Retrieve all Bidders associated with the default company and other companies and write them to a file
        """
        company_names = [
            "delivery_regression_traffic_shaping",
            self.__company_name_from_id(
                self.util_resources.authorization_context.company_id
            ),
        ]
        distinct_company_names = list(dict.fromkeys(company_names))

        self.__fetch_and_write_bidders_to_file(distinct_company_names)


BidderDataFile().generate()
