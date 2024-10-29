import csv
import logging
import os

from core.Routers import Routers
from core.RoutersConstants import REPLACE
from core.configuration import Configuration


class Data:
    def __init__(self, router_uid: str, demand_sources_uid):
        self.router_uid = router_uid
        self.demand_sources_uid = demand_sources_uid


class DemandSource:
    def __init__(self, guid):
        self.guid = guid
        self.number_of_execution = 0


class Case:
    def __init__(self, name: str, external_config=Configuration()):
        self.name = name
        self.inventory_routers = Routers(external_config)

        path_file_csv = os.getenv("RS_DATA_FILE", None)
        if path_file_csv is None:
            logging.error("The variable [RS_DATA_FILE] is not set in the environment")
            raise Exception("The variable [RS_DATA_FILE] is not set in the environment")

        with open(path_file_csv, newline="") as csvFile:
            data_file_reader = csv.reader(
                csvFile, quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            read_rows = 0
            for row in data_file_reader:
                if read_rows > 0 and row[0] == name:
                    self.inventory_routers.uid = row[1]
                    # It will convert the router id & demand sources uid to a data
                    self.data = Data(row[1], row[2].split(","))
                    break
                read_rows = read_rows + 1
            if self.inventory_routers.uid == REPLACE:
                raise ValueError(f"The case [{name}] is not found in the data file")
