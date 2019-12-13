from lgbsttracker.entities._lgbsttracker_object import _LGBSTTrackerObject
from lgbsttracker.protos.service_pb2 import LightSensor as ProtoLightSensor


class LightSensor(_LGBSTTrackerObject):
    """
    LightSensor object.
    """

    def __init__(self, light_sensor_id, name, value, creation_time, last_update_time):
        self._light_sensor_id = light_sensor_id
        self._name = name
        self._value = value
        self._creation_time = creation_time
        self._last_update_time = last_update_time

    @property
    def light_sensor_id(self):
        """String corresponding to the light sensor id."""
        return self._light_sensor_id

    @property
    def name(self):
        """String corresponding to the light sensor name."""
        return self._name

    @property
    def value(self):
        """Float value of the sensor."""
        return self._value

    @property
    def last_update_time(self):
        """Light sensor timestamp as an integer (milliseconds since the Unix epoch)."""
        return self._last_update_time

    @property
    def creation_time(self):
        """Light sensor timestamp as an integer (milliseconds since the Unix epoch)."""
        return self._creation_time

    def to_proto(self):
        light_sensor = ProtoLightSensor()
        light_sensor.light_sensor_id = self.light_sensor_id
        light_sensor.name = self.name
        light_sensor.value = self.value
        light_sensor.last_update_time = self.last_update_time
        light_sensor.creation_time = self.creation_time
        return light_sensor

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.key, proto.value, proto.timestamp)
