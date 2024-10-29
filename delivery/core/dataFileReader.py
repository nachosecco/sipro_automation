import csv
import logging


class DataFileReader:
    def __init__(self, path_file_csv):
        self.data = []

        with open(path_file_csv, newline="") as csvFile:
            data_file_reader = csv.reader(
                csvFile, quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            read_rows = 0
            for row in data_file_reader:
                if read_rows == 0:
                    self.headers = row
                else:
                    self.data.append(row)
                read_rows += 1

    def assign_data_file_values_to_case(self, case):
        for row in self.data:
            if row[0] == case.name:
                self.__assign(case, row)
                return True
        return False

    def __assign(self, case, row):
        logging.debug(f"assign values to the case {case.name}")
        column_index = 0
        for columnValue in row:
            if len(columnValue) == 0:  # //skip empty column values
                column_index += 1
                continue

            column_header = self.headers[column_index]
            if column_header.startswith("vpc_"):
                vpc_field = self.headers[column_index].replace("vpc_", "")
                setattr(case.vpc, vpc_field, columnValue)

            else:
                if column_header != "case":
                    logging.warning(
                        "We only support 2 columns, case name, uid for placement, and data from environment"
                    )

            column_index += 1
