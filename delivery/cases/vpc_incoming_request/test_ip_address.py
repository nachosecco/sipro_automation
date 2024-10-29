import pytest
from core.case import Case
from core.vastValidator import VastValidator
from core.utils.geoIpUtils import get_ip_for_geo


# Verify ip_address in query parameter values are correct in the VPC incoming request
@pytest.mark.regression
def test_query_param_ip_address():
    case = Case("test_query_param_ip_address")  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = "52.13.119.116"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # This will asssert that the value is passed
    vastResult.assertLogsDelivery(["ip_address=52.13.119.116"])


# Verify ip_address is reading from the header when it’s not passing from the query parameter
# this test case is removed from regression list as it is failing because of ip address on jenkins is different from local
@pytest.mark.smoke
def test_with_out_query_param_ip_address():
    case = Case(
        "test_with_out_query_param_ip_address"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = ""

    # This would execute the framework
    vastResult = VastValidator().test(vpc)

    # This will execute the all assertions in the case
    vastResult.assertCase(case)

    # Assert that the ipAddress contains a value
    vastResult.assertLogsDelivery(["ipAddress=52.13.119.116"])


# This would test a placement would throw 403 forbidden when the ipaddress passed belongs to european country .
@pytest.mark.regression
def test_with_ip_address_europe_forbidden():
    case = Case(
        "test_with_ip_address_europe_forbidden"
    )  # This is the file to test this case

    vpc = case.vpc
    vpc.ip_address = get_ip_for_geo(country="DE")

    # This would execute the framework
    vastResult = VastValidator().test(vpc, 403)
