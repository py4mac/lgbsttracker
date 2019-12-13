import unittest
import json
from lgbsttracker.server import app


class TestAPI(unittest.TestCase):
    def test_api_get_light_sensor_by_id(self):
        request, response = app.test_client.get("/api/v1/sensors/lightsensors/1")
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data, {"light_sensor": {"id": "1", "name": "my_sensor_light1"}})

    def test_api_get_light_sensors(self):
        request, response = app.test_client.get("/api/v1/sensors/lightsensors")
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(data, {"light_sensors": [{"id": "1", "name": "my_sensor_light1"}, {"id": "2", "name": "my_sensor_light2"}]})
