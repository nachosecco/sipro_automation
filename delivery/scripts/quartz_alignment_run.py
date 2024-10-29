import logging
import os

from core.quartz import Quartz


def setup_logger():
    logging.basicConfig(format="%(asctime)s [%(levelname)8.8s] %(message)s")

    logger = logging.getLogger("csv")
    logger.setLevel(logging.DEBUG)
    return logger


Quartz(os.environ.get("DFQ_SERVER_ROOT_URL"), setup_logger()).run_job(
    "alignment.AlignmentCacheRefreshJob"
)
