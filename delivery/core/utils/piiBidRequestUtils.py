from core.configuration import Configuration


def validate_rtb_ctv_common_properties(bid_request_validator):
    assert bid_request_validator.is_placement_type_as_expected("mobile")
    assert bid_request_validator.is_required_properties_valid()
    assert bid_request_validator.is_video_object_valid()
    assert bid_request_validator.is_app_object_valid()
    assert bid_request_validator.is_number_of_properties_as_expected(11)
    assert bid_request_validator.is_tmax_as_expected(Configuration().rtb_tmax)
    assert bid_request_validator.is_at_as_expected(2)
    assert bid_request_validator.is_allimps_as_expected(0)
    assert bid_request_validator.is_cur_as_expected(["USD"])


def get_expected_user_object():
    return {"geo": {}, "ext": {}}


# Returns expected Ext object as specified in RTB 2.2 in test bid requests
def get_expected_ext_object(root_domain):
    expected_ext = {
        "schain": {
            "ver": "1.0",
            "complete": 1,
            "nodes": [
                {
                    "asi": root_domain,
                    "sid": "REPLACE",
                    "hp": 1,
                    "rid": "REPLACE",
                }
            ],
        }
    }
    return expected_ext


def get_expected_device_object_rtb22():
    expected_device = {
        "geo": {},
        "dnt": 0,
        "os": "Other",
        "js": 0,
        "connectiontype": 0,
    }
    return expected_device


def get_expected_device_object_rtb23():
    expected_device = {
        "geo": {},
        "dnt": 0,
        "lmt": 0,
        "os": "Other",
        "js": 0,
        "connectiontype": 0,
    }
    return expected_device


def get_expected_device_object_rtb24():
    expected_device = get_expected_device_object_rtb23()
    expected_device["geofetch"] = 0
    return expected_device


def get_expected_device_object_rtb25():
    return get_expected_device_object_rtb24()


def get_expected_device_object_rtb26():
    return get_expected_device_object_rtb24()


def get_expected_source_object_rtb25(root_domain):
    expected_source = {
        "fd": 0,
        "tid": "REPLACE",
        "ext": {
            "schain": {
                "ver": "1.0",
                "complete": 1,
                "nodes": [
                    {
                        "asi": root_domain,
                        "sid": "REPLACE",
                        "hp": 1,
                        "rid": "REPLACE",
                    }
                ],
            }
        },
    }
    return expected_source


def get_expected_source_object_rtb26(root_domain):
    return get_expected_source_object_rtb25(root_domain)


def is_precise_location_fields_removed(geo_object):
    assert geo_object
    assert "lat" not in geo_object
    assert "lon" not in geo_object
    assert geo_object["zip"] is ""
