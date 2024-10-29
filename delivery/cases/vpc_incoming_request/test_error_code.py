import pytest
import requests
from core.utils.urlutils import get_delivery_url


@pytest.mark.regression
def test_error_status_when_placement_id_missing():
    url = get_delivery_url() + "/vast"
    response = requests.get(url)

    assert response.status_code == 400, "Status code expected on UID missing is 400"
    assert response.text.index("Required String parameter 'uid' is not present") > -1


@pytest.mark.regression
def test_error_status_when_placement_id_missing_in_dpl():
    url = get_delivery_url() + "/dpl?tid=2"
    response = requests.get(url)

    assert (
        response.status_code == 400
    ), "Status code expected on missing required param is 400"
    assert response.text.index("Required String parameter 'uid' is not present") > -1
