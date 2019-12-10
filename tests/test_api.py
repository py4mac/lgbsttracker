import unittest
from starlette.testclient import TestClient

from lgbsttracker.server import app

client = TestClient(app)


class TestAPI(unittest.TestCase):
    def test_read_main(self):
        response = client.get("/api/v1/items/1")
        assert response.status_code == 200
        assert response.json() == {"item": {"id": "1", "msg": "foo"}}
