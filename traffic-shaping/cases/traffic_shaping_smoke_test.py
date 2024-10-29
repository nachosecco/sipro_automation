import pytest
import logging
from datetime import datetime

from core.case import Case
from core.description import description
from core.utils.date_utils import get_past_hours
from core.utils.aerospike_utils import get_bins, BLOCKED_BIDDERS_BIN
import core.query.athena as athena


@description("Smoke test traffic shaping")
@pytest.mark.regression
def test_traffic_shaping_seed_data():
    case = Case("test_traffic_shaping_smoke_test")
    data_monitor_hour = "20200102_1100"
    prior_hours = get_past_hours(data_monitor_hour)
    execution_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    logging.debug("test_traffic_shaping_seed_data execution time: %s", execution_time)
    placement_guid = f"smoke_test_placement_guid-{execution_time}"
    app_bundle_id = f"smoke_test_app_bundle_id-{execution_time}"

    # bidder to be blocked should be named with a prefix "blocked"
    hourly_records = {
        prior_hours[0]: {
            "blocked": ["blocked_bidder_guid_1"],
            "allowed": ["allowed_bidder_guid_1"],
        },
        prior_hours[23]: {
            "blocked": ["blocked_bidder_guid_1"],
            "allowed": ["allowed_bidder_guid_1"],
        },
    }
    traffic_shaping = case.get_traffic_shaping_and_load_data(
        hourly_records, data_monitor_hour, placement_guid, app_bundle_id
    )
    assert traffic_shaping is not None

    # Programmatically trigger Data Monitor job and wait for Data Aggregator and Blocklist Generator jobs to complete
    traffic_shaping.trigger_dags_and_wait_for_completion(data_monitor_hour, case.name)

    # Verify that the blocked bidder is present in the traffic_shaping_hourly_blocklist table in Athena
    result = athena.get_traffic_shaping_hourly_blocklist_for_hour(
        case.configuration.athena_database, prior_hours[0]
    )
    assert result is not None
    # Exactly 2 rows (1 header row and 1 data row) mean there's one and only one blocked bidder
    assert athena.get_rows_count(result) == 2
    # Make sure blocked_bidder_guid_1 is the partner_guid value for the first row (0th row is the header row)
    partner_guid = athena.get_column_value_for_row(result, "partner_guid", 1)
    assert partner_guid == "blocked_bidder_guid_1"

    # Verify that the blocked bidder is present in the Aerospike cache and no other bidders are present
    # Build the aerospike key based on the placement name and app bundle id used in the data seeding
    bins = get_bins(placement_guid + app_bundle_id)
    # Record should be present in aerospike and blocked bidders bin should have the blocked bidder only
    assert bins is not None
    assert bins[BLOCKED_BIDDERS_BIN] == ["blocked_bidder_guid_1"]
