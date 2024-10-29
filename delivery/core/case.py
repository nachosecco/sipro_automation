import os

from core.adPodAssertor import adPod
from core.dataEnvironment import DataEnvironment
from core.dataFileReader import DataFileReader
from core.targeting import targeting
from core.vpc import VPC
from core.dto.event import Event


# This is the class to represent the case and all information of the case to test
class Case:
    def __init__(self, name: str):
        self.logDelivery = []
        self.logEvents = []
        self.vpc = VPC()
        self.media = []
        self.name = name
        self.assertionTargeting = targeting()

        self.adPod = adPod()
        self.event = Event()

        path_to_data_file = os.getenv("DATA_FILE")
        if path_to_data_file is None or len(path_to_data_file) == 0:
            raise Exception(
                "The Data file path is required, set the env variable `DATA_FILE`"
            )

        was_assigned = DataFileReader(
            path_to_data_file
        ).assign_data_file_values_to_case(self)
        if not was_assigned:
            raise Exception(
                f"The data file did not contain information to the case({name})"
            )

        self.data_environment = DataEnvironment(self.vpc.uid)
