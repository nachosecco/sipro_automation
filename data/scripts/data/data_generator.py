import argparse
import glob
import json
import logging
import os
import shutil
from typing import List

from core.util.data_csv_util import DataCsvUtil, DataPlacement


class DataGeneratorUtil:
    """Class used to copy and renaming the placement names"""

    def __init__(self, execution_id, origin_path, destination_path):
        self.execution_id = execution_id
        self.origin_path = os.path.abspath(origin_path)
        self.destination_path = os.path.abspath(destination_path)

    def copy(self):
        logging.info(
            "Will copy all the json files that are in cases to some path like build/data/json"
        )
        if not os.path.isdir(self.destination_path):
            os.makedirs(self.destination_path, exist_ok=True)

        for file_path in glob.glob(
            os.path.join(self.origin_path, "**", "*.json"), recursive=True
        ):
            new_path = os.path.join(self.destination_path, os.path.basename(file_path))
            shutil.copy(file_path, new_path)

    def rename_placement_with_suffix(self) -> List[str]:
        logging.info(
            "Renaming the placements to have the suffix [%s]",
            self.execution_id,
        )
        placement_names = []
        for file_path in glob.glob(
            os.path.join(self.destination_path, "**", "*.json"), recursive=True
        ):
            with open(file_path, "r+") as data_file:
                json_data_file = json.load(data_file)
                original_name = json_data_file["supply"]["placement"]["name"]
                placement_name = original_name + "_" + self.execution_id
                json_data_file["supply"]["placement"]["name"] = placement_name
                placement_names.append(placement_name)
                data_file.seek(0)
                json.dump(json_data_file, data_file, indent=2)
                data_file.truncate()
        return placement_names


class DataGenerator:
    """The use of this class is only to generate the new json files to be used by data-seed-upload"""

    def __init__(
        self, execution_id, origin_path, destination_path, destination_path_csv
    ):
        self.execution_id = execution_id
        self.origin_path = origin_path
        self.destination_path = destination_path
        self.destination_path_csv = destination_path_csv

    def generate(self):

        execution_id = self.execution_id

        json_data = DataGeneratorUtil(
            execution_id, self.origin_path, self.destination_path
        )
        json_data.copy()
        placements = json_data.rename_placement_with_suffix()

        logging.info("We are going to create csv file")

        DataGenerator.write_csv_without_uuid(self.destination_path_csv, placements)

    @staticmethod
    def write_csv_without_uuid(destination_path_csv, placements: List[str]):
        # we are writing a file, that will contain all cases, with an empty uid,
        # so when we create the placement we put the association there
        logging.info(
            "Converting placement names into the env data csv in build folder with [%s]",
            placements,
        )
        data_in_csv = []
        for placement in placements:

            data_in_csv.append(DataPlacement(placement, "", "", ""))

        DataCsvUtil(destination_path_csv).write(data_in_csv)


parser = argparse.ArgumentParser(
    prog="data_generator.py",
    description="A tool used to prepare to upload json data files",
)
parser.add_argument(
    "--execution_id",
    required=True,
    help="The common execution id to use as a suffix in the placements",
)

parser.add_argument(
    "--origin_path",
    required=True,
    help="The path from where to copy json ",
)


parser.add_argument(
    "--destination_path",
    required=True,
    help="The destination path to copy json ",
)

parser.add_argument(
    "--destination_path_csv",
    required=True,
    help="The destination path to write csv",
)

logging.basicConfig(level=logging.INFO)

args = parser.parse_args()
print(f"Parsed Arguments are: ${vars(args)}")

DataGenerator(
    args.execution_id,
    args.origin_path,
    args.destination_path,
    args.destination_path_csv,
).generate()
