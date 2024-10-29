import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.constants import REPLACE


# This would test that the channel and network are present in delivery logs.
@pytest.mark.regression
def test_channel_param():
    case = Case("test_channel_param")

    vpc = case.vpc
    vpc.channel_name = "BBC"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery([f"channel_name={vpc.channel_name}"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


@pytest.mark.regression
def test_network_param():
    case = Case("test_network_param")

    vpc = case.vpc
    vpc.network_name = "network_name"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery([f"network_name={vpc.network_name}"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


@pytest.mark.regression
def test_missing_channel_param():
    case = Case("test_missing_channel_param")

    vpc = case.vpc

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery([f"channel_name={REPLACE}"])


@pytest.mark.regression
def test_missing_network_param():
    case = Case("test_missing_network_param")

    vpc = case.vpc

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertCase(case)
    vastResult.assertLogsDelivery([f"network_name={REPLACE}"])
