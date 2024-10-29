from datetime import datetime

import pytest

from core.case import Case
from core.configuration import Configuration
from core.description import description
from core.util.app_utils import check_and_get_env


@description("Set up for the placeholder")
@pytest.mark.placeholder
def test_placeholder_setup():
    configuration = Configuration()
    configuration.csv_path_file = check_and_get_env("DPR_PATH_PLACEHOLDER_CSV")
    case = Case("test_placeholder", configuration)

    now = datetime.now()
    parameters = case.delivery_parameters
    parameters.content_title = "placeholder that was running at " + now.strftime(
        "%Y/%m/%d H:%M:%S"
    )

    event_coordinator = case.event_coordinator(case.delivery_controller().ctv())

    # will call delivery 1 time and return a list of events by each ad that was in the vast
    delivery_events = event_coordinator.call_delivery()

    # for placeholder, it should be only 1 ad
    for event in delivery_events.events:
        event.call_impression()
