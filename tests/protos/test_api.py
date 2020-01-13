import unittest

from lgbsttracker.protos.api_storage_sensors_service_pb2 import CreateLightSensor
from lgbsttracker.protos.sensors_message_pb2 import LightSensor


class TestLightSensorsApi(unittest.TestCase):
    def test_getlightsensors_response(self):
        response = CreateLightSensor.Response()
        proto = LightSensor()
        response.item.name = proto.name
        assert response is not None
