from lgbsttracker.utils.proto_utils import timestamp_to_datetime, datetime_to_seconds
from lgbsttracker.entities._lgbsttracker_object import _LGBSTTrackerObject
from lgbsttracker.protos.sensors_message_pb2 import LightSensor as ProtoLightSensor


class LightSensor(_LGBSTTrackerObject):
    """
    LightSensor object.
    """

    def __init__(self, light_sensor_id, name, value, creation_time, last_updated_time):
        self._light_sensor_id = light_sensor_id
        self._name = name
        self._value = value
        self._creation_time = creation_time
        self._last_updated_time = last_updated_time

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
    def last_updated_time(self):
        """Light sensor timestamp as an integer (milliseconds since the Unix epoch)."""
        return self._last_updated_time

    @property
    def creation_time(self):
        """Light sensor timestamp as an integer (milliseconds since the Unix epoch)."""
        return self._creation_time

    def to_proto(self):
        light_sensor = ProtoLightSensor()
        light_sensor.name = self.name
        if self.value:
            light_sensor.value = self.value
        if self.last_updated_time:
            light_sensor.last_updated_time.seconds = datetime_to_seconds(self.last_updated_time)
        light_sensor.creation_time.seconds = datetime_to_seconds(self.creation_time)
        return light_sensor

    @classmethod
    def from_proto(cls, proto):
        return cls(
            proto.light_sensor_id, proto.name, proto.value, timestamp_to_datetime(proto.creation_time), timestamp_to_datetime(proto.last_updated_time)
        )
