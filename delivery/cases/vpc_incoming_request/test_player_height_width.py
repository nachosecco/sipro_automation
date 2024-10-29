import pytest
from core.case import Case
from core.vastValidator import VastValidator


# This would test that player_height is correctly populated in vpc incoming request in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_player_height():
    case = Case("test_player_height")  # This is the file to test this case

    vpc = case.vpc
    vpc.player_height = "600"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["player_height=600"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


# This would test that player_width is correctly populated in vpc incoming request in delivery logs.
@pytest.mark.regression
def test_player_width():
    case = Case("test_player_width")  # This is the file to test this case

    vpc = case.vpc
    vpc.player_width = "800"

    # This would execute the framework
    vastResult = VastValidator().test(vpc)
    vastResult.assertLogsDelivery(["player_width=800"])

    # This will execute the all assertions in the case
    vastResult.assertCase(case)


# This would test that when invalid player_height is passed in placement tag correct error is showing in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_player_invalid_height():
    case = Case("test_player_invalid_height")  # This is the file to test this case

    vpc = case.vpc
    vpc.player_height = "abc"

    vastResult = VastValidator().test(vpc, 400)  # This would execute the framework.
    vastResult.assertLogsDelivery(["Invalid width and/or height."])
    vastResult.assertCase(case)  # This will execute the all assertions in the case.


# This would test that when invalid player_width is passed in placement tag correct error is showing in delivery logs.
@pytest.mark.regression
def test_player_invalid_width():
    case = Case("test_player_invalid_width")  # This is the file to test this case

    vpc = case.vpc
    vpc.player_width = "abc"

    vastResult = VastValidator().test(vpc, 400)  # This would execute the framework
    vastResult.assertLogsDelivery(["Invalid width and/or height."])

    vastResult.assertCase(case)  # This will execute the all assertions in the case


# This would test that when player_height is missing in placement tag then correct error is showing in delivery logs.
@pytest.mark.regression
@pytest.mark.smoke
def test_player_missing_height():
    case = Case("test_player_missing_height")  # This is the file to test this case

    vpc = case.vpc
    vpc.player_height = ""

    vastResult = VastValidator().test(vpc, 400)  # This would execute the framework
    vastResult.assertLogsDelivery(["Invalid width and/or height."])
    vastResult.assertCase(case)  # This will execute the all assertions in the case


# This would test that when player_width is missing in placement tag then correct error is showing in delivery logs.
@pytest.mark.regression
def test_player_missing_width():
    case = Case("test_player_missing_width")  # This is the file to test this case

    vpc = case.vpc
    vpc.player_width = ""

    vastResult = VastValidator().test(vpc, 400)  # This would execute the framework
    vastResult.assertLogsDelivery(["Invalid width and/or height."])
    vastResult.assertCase(case)  # This will execute the all assertions in the case
