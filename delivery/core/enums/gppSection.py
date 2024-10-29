from enum import Enum


# class syntax
class GPPSection(Enum):
    US_NATIONAL = "7"
    VIRGINIA = "9"
    COLORADO = "10"
    UTAH = "11"
    CONNECTICUT = "12"

    def __init__(self, id):
        self.id = id
