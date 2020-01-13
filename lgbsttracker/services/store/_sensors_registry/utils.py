from __future__ import print_function

import os
import sys

from lgbsttracker.protos.common_pb2 import INTERNAL_ERROR
from lgbsttracker.exceptions import LgbsttrackerException
from lgbsttracker.services.store._sensors_registry.registry import SensorStoreRegistry
from lgbsttracker.utils import env
from lgbsttracker.utils.file_utils import path_to_local_file_uri

_SENSOR_URI_ENV_VAR = "LGBSTTRACKER_SENSOR_URI"

# Extra environment variables
_SENSOR_USERNAME_ENV_VAR = "LGBSTTRACKER_SENSOR_USERNAME"
_SENSOR_PASSWORD_ENV_VAR = "LGBSTTRACKER_SENSOR_PASSWORD"

_sensor_uri = None


def is_sensor_uri_set():
    """Returns True if the Sensor URI has been set, False otherwise."""
    if _sensor_uri or env.get_env(_SENSOR_URI_ENV_VAR):
        return True
    return False


def set_sensor_uri(uri):
    """
    Set the Sensor URI.
    :param uri: Input parameter string
    """
    global _sensor_uri
    _sensor_uri = uri


def get_sensor_uri():
    """
    Get the Sensor URI.

    :return: The Sensor URI.
    """
    global _sensor_uri
    if _sensor_uri is not None:
        return _sensor_uri
    elif env.get_env(_SENSOR_URI_ENV_VAR) is not None:
        return env.get_env(_SENSOR_URI_ENV_VAR)
    else:
        raise LgbsttrackerException(f"Variable {_SENSOR_URI_ENV_VAR} is not set", error_code=INTERNAL_ERROR)


def _get_sqlalchemy_store(sensor_uri):
    from lgbsttracker.store.sensors.sqlalchemy_store import SqlAlchemyStore

    return SqlAlchemyStore(db_uri=sensor_uri)


_sensor_store_registry = SensorStoreRegistry()
_sensor_store_registry.register("sqlite", _get_sqlalchemy_store)
_sensor_store_registry.register("postgresql", _get_sqlalchemy_store)
_sensor_store_registry.register_entrypoints()


def _get_store(sensor_uri=None):
    return _sensor_store_registry.get_store(sensor_uri)
