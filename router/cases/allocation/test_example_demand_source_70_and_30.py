import pytest

from core.Case import Case
from core.Description import description
from core.RouterValidator import ValidatorConfig, Validator


@pytest.mark.regression
@description(
    """It will execute 30 times with an approximation_error of 1% of error
    and expect to 1 demand source with 70% and the other with 30% """
)
def test_get_inventory_routers_ok():
    case = Case("test_get_inventory_routers_ok")  # This is the file to test this case

    # With this instance we can send all parameters to Inventory Routers
    inventory_routers = case.inventory_routers

    # With this config, it will execute 30 times, with an approximation_error of 1%
    config = ValidatorConfig(30, 1)

    # This would execute the framework
    result = Validator().test(inventory_routers, config)

    # Taking all demand sources the guid into variables
    guid1 = case.data.demand_sources_uid[0]
    guid2 = case.data.demand_sources_uid[1]

    # This would assert that 2 demand sources execution has a similar allocation
    result.assert_demand_sources(
        {
            guid1: 70,
            guid2: 30,
        }
    )

    # The inventory_router_results is an array all results execution in Delivery
    # Taking the first execution for the example
    inventory_router_result = result.inventory_router_results[0]

    # This is to assert that is used for test Delivery's
    vast_result = inventory_router_result.vast_result_assert

    vast_result.assert_vast_xml().assert_not_empty()
