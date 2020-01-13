"""
Internal package providing a Python CRUD interface.
"""

import time
import os
from six import iteritems

from lgbsttracker.entities.light_sensor import LightSensor
from lgbsttracker.services.store._sensors_registry import utils


class SensorService(object):
    """
    Sensor Service.
    """

    def __init__(self, sensor_uri):
        """
        :param sensor_uri: Address of local or remote sensor db.
        """
        self.sensor_uri = sensor_uri
        self.store = utils._get_store(self.sensor_uri)

    def create_light_sensor(self, name):
        """
        Create light sensor.

        :param name: Light Sensor Name

        :return: A :py:class:`lgbsttracker.entities.LightSensor` object.
        """
        return self.store.create_light_sensor(name)
