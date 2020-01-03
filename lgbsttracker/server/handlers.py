import json
import os
import re
import six
from functools import wraps

from functools import wraps
from querystring_parser import parser
from sanic import response
from sanic.request import Request

from lgbsttracker.exceptions import LgbsttrackerException
from lgbsttracker.utils.proto_json_utils import parse_dict, message_to_json
from lgbsttracker.protos.api_storage_sensors_service_pb2 import StorageSensorsApi, GetLightSensorById, GetLightSensors, CreateLightSensor
from lgbsttracker.protos.lightsensor_message_pb2 import LightSensor
from google.api.annotations_pb2 import http


def _not_implemented():
    return response.json(status_code=404)


def _get_path(base_path):
    path = "/api/v1{}".format(base_path)
    # path path as sanic expect parameters with <> pattern
    path = path.replace("}", ">")
    path = path.replace("{", "<")
    return path


def get_handler(request_class):
    """
    :param request_class: The type of protobuf message
    :return:
    """
    return HANDLERS.get(request_class, _not_implemented)


def _search_endpoints(http_rule):
    """ Return method, path. """
    if http_rule.get != "":
        return ["GET"], _get_path(http_rule.get)
    elif http_rule.put != "":
        return ["PUT"], _get_path(http_rule.put)
    elif http_rule.get != "":
        return ["POST"], _get_path(http_rule.post)
    elif http_rule.get != "":
        return ["DELETE"], _get_path(http_rule.delete)
    elif http_rule.get != "":
        return ["PATCH"], _get_path(http_rule.patch)
    return [], None


def get_endpoints():
    """
    :return: List of tuples (path, handler, methods)
    """

    def get_service_endpoints(service):
        ret = []
        for service_method in service.DESCRIPTOR.methods:
            http_rule = service_method.GetOptions().Extensions[http]
            method, http_path = _search_endpoints(http_rule)
            handler = get_handler(service().GetRequestClass(service_method))
            if (len(method) == 1) and (http_path != ""):
                ret.append((http_path, handler, method))
        return ret

    return get_service_endpoints(StorageSensorsApi)


def _get_request_message(request_message, aiohttp_request):
    request_json = aiohttp_request

    if isinstance(request_json, six.string_types):
        request_json = json.loads(request_json)

    if request_json is None:
        request_json = {}
    parse_dict(request_json, request_message)
    return request_message


def _get_route_info(request_message, request):
    import json

    req = request.match_info
    parse_dict(req, request_message)
    return request_message


def catch_lgbsttracker_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LgbsttrackerException as e:
            return response.json(e.serialize_as_json(), status_code=e.get_http_status_code())

    return wrapper


@catch_lgbsttracker_exception
def _get_light_sensor_by_id(request: Request, id):
    request_message = _get_route_info(GetLightSensorById(), request)
    # Eg: You can access to request_message field id for ex
    response_message = GetLightSensorById.Response()
    response_message.item.id = "1"
    response_message.item.name = "my_sensor_light1"
    return response.text(message_to_json(response_message))


def GetItemsModel_to_GetItem(result):
    return Item(id=result.id, msg=result.msg)


@catch_lgbsttracker_exception
def _get_light_sensors(request: Request):
    request_message = _get_route_info(GetLightSensors(), request)
    # Eg: You can access to request_message field id for ex
    response_message = GetLightSensors.Response()
    response_message.items.extend([LightSensor(id="1", name="my_sensor_light1"), LightSensor(id="2", name="my_sensor_light2")])
    return response.text(message_to_json(response_message))


@catch_lgbsttracker_exception
def _create_light_sensor(request: Request):
    request_message = _get_request_message(CreateLightSensor(), request)
    # Eg: Store here the item inside your DB ...
    response_message = CreateLightSensor.Response()
    response_message.item.id = "1"
    response_message.item.name = request_message.item.msg
    return response.json(message_to_json(response_message))


HANDLERS = {
    # Tracking Server APIs
    GetLightSensorById: _get_light_sensor_by_id,
    GetLightSensors: _get_light_sensors,
    CreateLightSensor: _create_light_sensor,
}
