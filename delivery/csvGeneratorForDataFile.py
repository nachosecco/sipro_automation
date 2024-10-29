# It will search all json files in the case files, and would try to generate a csv with this information
import csv
import json
import logging
import os
from os.path import exists

from core.configuration import Configuration
from core.utilResources import UtilResources, Company

HEADER_UID = "vpc_uid"
HEADER_CASE = "case"
HEADERS_COLUMNS = [HEADER_CASE, HEADER_UID]
CSV_HEADERS = ",".join(HEADERS_COLUMNS)
CSV_COLUMN_INDEX_CASE_GUID = HEADERS_COLUMNS.index(HEADER_UID)
CSV_COLUMN_INDEX_CASE_NAME = HEADERS_COLUMNS.index(HEADER_CASE)
DEFAULT_COMPANY_NAME = "_DEFAULT_COMPANY_NAME"


class CsvGenerator:
    def __init__(self, configuration=Configuration()):
        self.__setup_logger()
        self.util_resources = UtilResources()
        self.configuration = configuration
        self.company_cache = Company(self.util_resources).get_companies()
        self.alignments_cache = {
            DEFAULT_COMPANY_NAME: self.find_all_alignments_for_company(
                DEFAULT_COMPANY_NAME
            )
        }
        self.placement_cache = {
            DEFAULT_COMPANY_NAME: self.find_all_placements_for_company(
                DEFAULT_COMPANY_NAME
            )
        }

    def __setup_logger(self):
        logging.basicConfig(format="%(asctime)s [%(levelname)8.8s] %(message)s")

        logger = logging.getLogger("csv")
        logger.setLevel(logging.DEBUG)

        self.logger = logger

    def __get_placement(self, company_name, placement_name):
        if company_name not in self.placement_cache:
            self.placement_cache[company_name] = self.find_all_placements_for_company(
                company_name
            )
            self.alignments_cache[company_name] = self.find_all_alignments_for_company(
                company_name
            )

        return self.placement_cache[company_name].get(placement_name, None)

    def find_all_data_files_in_cases(self):
        self.logger.info("Starting to search case data files")
        files_found = []
        for root, dirs, files in os.walk("cases"):
            for file in files:
                if file.endswith(".json"):
                    files_found.append(os.path.join(root, file))

        self.logger.info(f"Found {len(files_found)} data files")
        return files_found

    def find_case_names_and_files(self):
        found_cases = []
        files = self.find_all_data_files_in_cases()
        for file in files:
            with open(file, "r+") as data_file:
                data = json.load(data_file)
                supply = data.get("supply")
                if supply is None:
                    continue
                placement = supply.get("placement")
                override_options = data.get("override_options", {})
                found_cases.append(
                    {
                        "name": placement.get("name"),
                        "dataFile": file,
                        "override_options": override_options,
                    }
                )

        self.logger.debug(f"Found data files {found_cases}")
        return found_cases

    def find_all_placements_for_company(self, company_name):
        self.logger.info(f"Finding all placements for company: {company_name}")
        if company_name != DEFAULT_COMPANY_NAME:
            company_id = self.company_cache.get(company_name, {}).get("id", None)
            placements = self.util_resources.supply.find_placements_by_index(
                company_id=company_id
            )
        else:
            placements = self.util_resources.supply.find_placements_by_index()
        return self.util_resources.collection_resources_to_dict_by_name(placements)

    def find_all_alignments_for_company(self, company_name):
        self.logger.info(f"Finding all placements for company: {company_name}")

        if company_name != DEFAULT_COMPANY_NAME:
            company_id = self.company_cache.get(company_name, {}).get("id", None)
            alignments = self.util_resources.supply.find_all_alignment_placements(
                company_id=company_id
            )
        else:
            alignments = self.util_resources.supply.find_placements_by_index()
        return self.util_resources.collection_resources_to_dict_by_key(
            alignments, "idPlacement"
        )

    # We are assuming the case is already in the environment.
    def find_case_and_placements(self):
        self.logger.info("Find all cases and placements")
        cases = self.find_case_names_and_files()
        cases_guid = []
        for case in cases:
            override_options = case["override_options"]
            company_name = override_options.get("company_name", DEFAULT_COMPANY_NAME)

            case_name = case.get("name")
            placement = self.__get_placement(company_name, case.get("name"))
            if placement is None:
                logging.warning(
                    f"Not found a placement with the case name[{case_name}]"
                )
            else:
                cases_guid.append({"case": case, "guid": placement.get("guid")})

                if self.alignments_cache.get(placement.get("id")) is None:
                    logging.warning(f"The placement with {case_name} is not align")

        self.logger.debug(f"Found {len(cases_guid)} cases and placements")
        return cases_guid

    def generate_or_replace_csv(self):

        cases_and_placements = self.find_case_and_placements()
        data_file_path = f"data/data-file-env-{self.configuration.environment}.csv"
        self.logger.info(f"Generating csv file {data_file_path}")
        rows = []
        cases_in_data_file = []
        data_file_exists = exists(data_file_path)
        if data_file_exists:
            self.logger.debug("Reading existing data file ")
            with open(data_file_path, "r+") as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    rows.append(row)
            for row in rows:
                for case_placement in cases_and_placements:
                    case = case_placement.get("case")
                    if case.get("name") == row[CSV_COLUMN_INDEX_CASE_NAME]:
                        self.write_to_row(case_placement, row)

                        cases_in_data_file.append(case_placement)
                        break

        new_lines_count = 0
        if not data_file_exists:
            rows.append(CSV_HEADERS.split(","))
        for case_placement in cases_and_placements:
            if case_placement not in cases_in_data_file:
                case = case_placement.get("case")

                rows.append([case.get("name"), case_placement.get("guid")])
                new_lines_count += 1

        with open(data_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

        self.logger.info(
            f"it was generated the csv file {data_file_path}. "
            f"Updated lines {len(cases_in_data_file)} and added {new_lines_count} lines"
        )

    @staticmethod
    def write_to_row(case_placement, row):

        row[CSV_COLUMN_INDEX_CASE_GUID] = case_placement.get("guid")


CsvGenerator().generate_or_replace_csv()
