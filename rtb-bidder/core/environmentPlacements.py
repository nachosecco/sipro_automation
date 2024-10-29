import os
import json


class EnvironmentPlacements:
    _instance = None

    def __new__(cls, file_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = cls._instance._load_json(file_path)
        return cls._instance

    def _load_json(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def get_for(self, key):
        return self._data.get(key, None)


environment_placements = EnvironmentPlacements(
    f'data/data-file-env-{os.getenv("RTBRT_ENVIRONMENT", "dev")}.json'
)
