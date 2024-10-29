import logging

import pytest

from core.case import Case
from core.description import description
from core.query.tables.druid.druid_common_metrics import CommonMetricsDruid
from core.query.tables.druid.druid_network_metrics import NetworkMetricsDruid


@description("Set up many tables example")
@pytest.mark.setup
def test_many_set_up():
    case = Case("test_many_tables")

    parameters = case.delivery_parameters
    parameters.content_series = "mock example"

    event_coordinator = case.event_coordinator(case.delivery_controller().ctv())

    # will call delivery 1 time and return a list of events by each ad that was in the vast
    delivery_events = event_coordinator.call_delivery()

    # will send all 3 event impression events, by each ad returned in the vast
    for event in delivery_events.events:
        event.call_impression(3)

    logging.info(f"Total events: {event_coordinator.total_events}")
    logging.info(f"Min date time: {event_coordinator.min_date_time}")
    logging.info(f"Max date time: {event_coordinator.max_date_time}")


@description("Many tables example")
@pytest.mark.regression
def test_many_tables():
    case = Case("test_many_tables")

    # Expected values for all 3 tables
    expected_opportunities = 1
    expected_impressions = 3
    expected_gross_revenue = 0.03

    # Assert in Network
    assert_in_network(
        case, expected_opportunities, expected_impressions, expected_gross_revenue
    )

    # Assert in Campaign
    assert_in_campaign(case, expected_impressions)

    # Assert in RTB
    assert_in_rtb(case, 0)

    # Assert in Athena
    athena_asserter = case.assert_in_athena()

    athena_asserter.opportunity().query_of_count_equals_to(expected_opportunities)
    athena_asserter.impression().query_of_count_equals_to(expected_impressions)


def assert_in_network(
    case, expected_opportunities, expected_impressions, expected_gross_revenue
):
    druid_asserter_network = case.assert_in_druid().network()

    # example single row of sum
    druid_asserter_network.query_of_sum_metrics_and_dimensions_with_single_row_equals_to(
        [NetworkMetricsDruid.OPPORTUNITY, CommonMetricsDruid.IMPRESSION],
        [],  # no dimension
        [expected_opportunities, expected_impressions],
    )

    # example multiple row, with no dimensions and of multiple aggregation
    druid_asserter_network.query_of_metrics_and_dimensions_with_equals_to(
        [
            CommonMetricsDruid.IMPRESSION,
            NetworkMetricsDruid.G_REVENUE,
        ],
        [],  # no dimension
        [[expected_impressions, expected_gross_revenue]],  # a single row
    )


def assert_in_campaign(case, expected_impressions):
    druid_asserter_campaign = case.assert_in_druid().campaign()

    # example single row of sum
    druid_asserter_campaign.query_of_sum_metrics_and_dimensions_with_single_row_equals_to(
        [CommonMetricsDruid.IMPRESSION],
        [],  # no dimension
        [expected_impressions],
    )

    # example multiple row, with no dimensions and of multiple aggregation
    druid_asserter_campaign.query_of_metrics_and_dimensions_with_equals_to(
        [CommonMetricsDruid.IMPRESSION],
        [],  # no dimension
        [[expected_impressions]],  # a single row
    )


def assert_in_rtb(case, expected_impressions):
    druid_asserter_rtb = case.assert_in_druid().rtb()

    # example single row of sum
    druid_asserter_rtb.query_of_sum_metrics_and_dimensions_with_single_row_equals_to(
        [CommonMetricsDruid.IMPRESSION],
        [],  # no dimension
        [expected_impressions],
    )

    # example multiple row, with no dimensions and of multiple aggregation
    druid_asserter_rtb.query_of_metrics_and_dimensions_with_equals_to(
        [CommonMetricsDruid.IMPRESSION],
        [],  # no dimension
        [[expected_impressions]],  # a single row
    )
