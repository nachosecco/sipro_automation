import logging
import os
from urllib.parse import urlparse, parse_qs, unquote

from core.constants import NOT_FOUND


def extract_query_param(param_name: str, url: str):
    if url is None:
        logging.error("url was found as empty, query param couldn't be extracted")
        return ""

    query_params = parse_qs(urlparse(url).query, keep_blank_values=True)
    logging.debug(
        "Query params are : %s and the param name : %s ", query_params, param_name
    )
    param_values = query_params.get(param_name, [])
    value = unquote(next(iter(param_values), NOT_FOUND))
    return value


def get_delivery_url():
    root_url_delivery = "DELIVERY_ROOT_URL"

    if root_url_delivery in os.environ:
        logging.debug(f"{root_url_delivery} value is {os.environ[root_url_delivery]}")

    else:
        logging.error(
            f"{root_url_delivery} does not exist, add env variable DELIVERY_ROOT_URL"
        )
        raise ValueError("There is not define env variable DELIVERY_ROOT_URL")

    return os.environ[root_url_delivery]
