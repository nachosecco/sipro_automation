import json


class Reader:
    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file

    def read(self):
        file = self.path_to_file
        f = open(file, "r")
        data = json.load(f)
        f.close()
        return data
