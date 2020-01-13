import json
import uuid

import mock
import pytest

import lgbsttracker
from lgbsttracker.server.handlers_utils import catch_lgbsttracker_exception
from lgbsttracker.server.endpoints.storage_sensors import get_endpoints, _create_light_sensor
from lgbsttracker.protos.common_pb2 import INTERNAL_ERROR, ErrorCode
from lgbsttracker.exceptions import LgbsttrackerException


@pytest.fixture()
def mock_get_sensor_service():
    with mock.patch("lgbsttracker.server.endpoints.storage_sensors._get_sensor_service") as m:
        yield m


def test_get_endpoints():
    endpoints = get_endpoints()
    create_light_sensor_endpoint = [e for e in endpoints if e[1] == _create_light_sensor]
    assert len(create_light_sensor_endpoint) == 1


def test_all_model_registry_endpoints_available():
    endpoints = {handler: method for (path, handler, method) in get_endpoints()}
    print(endpoints)

    # Test that each of the handler is enabled as an endpoint with appropriate method.
    expected_endpoints = {"POST": [_create_light_sensor]}
    # TODO: efficient mechanism to test endpoint path
    for method, handlers in expected_endpoints.items():
        for handler in handlers:
            assert handler in endpoints
            assert endpoints[handler] == method


def test_catch_lgbsttracker_exception():
    import json

    @catch_lgbsttracker_exception
    def test_handler():
        raise LgbsttrackerException("test error", error_code=INTERNAL_ERROR)

    # pylint: disable=assignment-from-no-return
    response = test_handler()
    assert response.status == 500
    json_response = json.loads(response.text)
    assert json_response["error_code"] == ErrorCode.Name(INTERNAL_ERROR)
    assert json_response["message"] == "test error"

