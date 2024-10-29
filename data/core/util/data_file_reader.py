import csv


class DataFileReader:
    def __init__(self, path_file_csv: str):
        self.data = []

        with open(path_file_csv, newline="") as csvFile:
            data_file_reader = csv.reader(
                csvFile, quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            read_rows = 0
            for row in data_file_reader:
                self.data.append(row)
                read_rows += 1
