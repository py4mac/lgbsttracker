import json
import os
import re
import six
from functools import wraps
from querystring_parser import parser
from aiohttp import web
from google.api.annotations_pb2 import http

from lgbsttracker.server.handlers_utils import (
    get_args_info,
    get_route_info,
    get_request_info,
    catch_lgbsttracker_exception,
    async_catch_lgbsttracker_exception,
)
from lgbsttracker.utils.proto_utils import message_to_json
from lgbsttracker.protos.api_storage_sensors_service_pb2 import StorageSensorsApi, CreateLightSensor
from lgbsttracker.services.store._sensors_registry.service import SensorService
from lgbsttracker.utils.rest_utils import search_endpoints

_sensor_service = None


def _get_sensor_service(uri=None):
    from lgbsttracker.services.store._sensors_registry import utils

    global _sensor_service
    if _sensor_service is None:
        sensor_uri = uri or utils.get_sensor_uri()
        _sensor_service = SensorService(sensor_uri)
    return _sensor_service


def init():
    pass


def _not_implemented():
    return web.json_response(status=404)


def _get_path(base_path):
    path = f"{base_path}"
    return path


def get_handler(request_class):
    """
    :param request_class: The type of protobuf message
    :return:
    """
    return HANDLERS.get(request_class, _not_implemented)


def get_endpoints():
    """
    :return: List of tuples (path, handler, methods)
    """

    def get_service_endpoints(service):
        ret = []
        for service_method in service.DESCRIPTOR.methods:
            http_rule = service_method.GetOptions().Extensions[http]
            method, http_path = search_endpoints(http_rule)
            handler = get_handler(service().GetRequestClass(service_method))
            if (len(method) == 1) and (http_path != ""):
                ret.append((_get_path(http_path), handler, method[0]))
        return ret

    return get_service_endpoints(StorageSensorsApi)


@async_catch_lgbsttracker_exception
async def _create_light_sensor(request):
    request_message = await get_request_info(CreateLightSensor(), request)
    response_message = CreateLightSensor.Response()
    item = _get_sensor_service().create_light_sensor(name=request_message.name)
    proto = item.to_proto()
    response_message.item.name = proto.name
    response_message.item.creation_time.seconds = proto.creation_time.seconds
    response_message.item.last_updated_time.seconds = proto.last_updated_time.seconds
    response_message.item.value = proto.value
    return web.json_response(text=message_to_json(response_message))


HANDLERS = {
    # Server APIs
    CreateLightSensor: _create_light_sensor
}
