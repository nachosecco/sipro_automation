import csv
import logging
from pathlib import Path
from typing import List

from core.case_context import CaseContext
from core.data_exception import DataException

DATA_FILE_PATH = "build/data/case_placements.csv"


class CsvObject:
    """Class that contains the rows of the csv file"""

    def __init__(self, rows):
        self.rows = rows


class DataPlacement:
    """Class to write/read csv files"""

    def __init__(self, name, uid, min_hour, max_hour):
        self.name = name
        self.uid = uid
        self.min_hour = min_hour
        self.max_hour = max_hour


class DataCsvUtil:
    """Class used to write and read the data
    generated when the placements were created"""

    def __init__(self, path: str):
        self.content = None
        self.path = path

    def get_case(self, case):
        for row in self.content.rows:
            if row[0] == case:
                return row
        raise DataException(f"Case not found: {case}")

    def read(self):

        if self.path is None or len(self.path) == 0:
            raise DataException(
                "The Data file path is required, make sure to set it properly."
            )

        data = []
        with open(self.path, newline="") as csv_file:
            data_file_reader = csv.reader(
                csv_file, quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            read_rows = 0
            for row in data_file_reader:
                data.append(row)
                read_rows += 1
        self.content = CsvObject(data)

        logging.info("csv data file %s and the content is %s", self.path, data)
        return self

    def write(self, csv_cases: List[DataPlacement]):
        path = self.path
        logging.info("We are going to write csv file %s", path)

        directory = path[0 : path.rfind("/")]
        Path(directory).mkdir(parents=True, exist_ok=True)

        with open(self.path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for csv_case in csv_cases:
                writer.writerow(
                    [
                        csv_case.name,
                        csv_case.uid,
                        # The min Hour should be the moment of the first request to the delivery
                        # The max Hour should be the moment of the last request to the event app
                        csv_case.min_hour,
                        csv_case.max_hour,
                    ]
                )


def load_case_context(case_name, path=DATA_FILE_PATH):
    if path is None:
        path = DATA_FILE_PATH
    case_csv_data = DataCsvUtil(path).read().get_case(case_name)
    logging.info(
        "Loading the case[%s] for in the file [%s] and the row %s",
        case_name,
        path,
        case_csv_data,
    )
    # we should use that data for lookup the placement_guid
    return CaseContext(
        case_csv_data[1], min_hour=case_csv_data[2], max_hour=case_csv_data[3]
    )
