import unittest

from lgbsttracker.protos.api_storage_sensors_service_pb2 import GetLightSensors
from lgbsttracker.protos.lightsensor_message_pb2 import LightSensor


class TestLightSensorsApi(unittest.TestCase):
    def test_getlightsensors_response(self):
        response = GetLightSensors.Response()
        response.items.append(LightSensor())
        assert response is not None
