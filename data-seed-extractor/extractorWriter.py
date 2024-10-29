import json
import logging
from abc import abstractmethod

from context import Context


class ExtractorWriter:
    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    def extract(self):
        pass

    def to_json(self):
        return json.dumps((self.extract()), indent=2)

    def write_to_folder(self):
        logger = logging.getLogger("extractor")

        logger.info("Converting to json")

        json_data = self.to_json()

        path = f"{self.context.folder_to_write}{self.context.case_name}.json"

        logger.info(f"Writing to file in {path}")

        f = open(path, "w")
        f.write(str(json_data))
        f.close()
