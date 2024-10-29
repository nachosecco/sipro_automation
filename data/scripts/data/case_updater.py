import argparse
import csv
import json
import logging
import os

from core.data_exception import DataException


class CaseUpdater:
    """Class to update the min/max dates of csv file"""

    def __init__(
        self,
        cases_dir,
        case_placement_file,
    ):
        self.event_json_dir = cases_dir
        self.case_placement_file = case_placement_file

    def update(self):
        files = []
        for file in os.listdir(self.event_json_dir):
            if file.endswith(".json"):
                files.append(file)

        events_data = {}
        for file_event_path in files:
            with open(self.event_json_dir + file_event_path) as file_event:
                event_data = json.load(file_event)
                events_data[event_data.get("case")] = {
                    "min_date": event_data.get("min_date"),
                    "max_date": event_data.get("max_date"),
                }

        logging.info("Events that are going to update %s", events_data)

        self.update_csv(events_data)

    def update_csv(self, events_data):
        # Read the CSV file into memory
        with open(self.case_placement_file, mode="r") as file:
            rows = list(csv.reader(file))

        # Find the row that matches the search_value in the first column
        logging.info(f"Total rows: {len(rows)}")
        for row in rows:
            logging.info(f"Updating row {row}")
            case = row[0]
            dates = events_data.get(case, None)
            if dates is None:
                msg = f"Could not find case '{case}' in file {self.case_placement_file} to update min/max dates."
                logging.error(msg)
                raise DataException(msg)
            min_date = dates.get("min_date")
            max_date = dates.get("max_date")
            if len(row) < 4:
                row.append(min_date)
                row.append(max_date)
            else:
                row[2] = min_date
                row[3] = max_date

        # Write the updated rows back to the CSV file
        with open(self.case_placement_file, mode="w", newline="") as file:
            csv.writer(file).writerows(rows)


parser = argparse.ArgumentParser(
    prog="case_updater.py",
    description="This will update the csv with min/max dates",
)
parser.add_argument(
    "--folder_event",
    required=True,
    help="The root path of the files of execution of events",
)
parser.add_argument(
    "--csv_file",
    required=True,
    help="The path of the file csv (name/uid) to add min and max",
)
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
CaseUpdater(args.folder_event, args.csv_file).update()
