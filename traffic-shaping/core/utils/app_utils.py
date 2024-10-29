import os

from core.data_exception import DataException


def check_and_get_env(name):
    val = os.getenv(name)

    if val is None or len(val) == 0:
        raise DataException(f"Empty environment variable: {name}.")

    return val
