import json
import os
import re
import six
from functools import wraps

from functools import wraps
from querystring_parser import parser
# from aiohttp.web import Request, Response
from starlette.requests import Request
from starlette.responses import Response

from lgbsttracker.utils.proto_json_utils import parse_dict, message_to_json
from lgbsttracker.server.protos.rest.service_pb2 import RestApi
from lgbsttracker.server.protos.rest.item_pb2 import GetItem, GetItems, PostItem, Item
from lgbsttracker.server.protos.rest import generic_pb2


def _not_implemented():
    return Response(media_type='application/json', status_code=404)


def _get_paths(base_path):
    """
    A service endpoints base path is typically something like /preview/mlflow/experiment.
    We should register paths like /api/v1/items/{id} in the Flask router.
    """
    return ['/api/v1{}'.format(base_path)]


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
            endpoints = service_method.GetOptions(
            ).Extensions[generic_pb2.rpc].endpoints
            for endpoint in endpoints:
                for http_path in _get_paths(endpoint.path):
                    handler = get_handler(
                        service().GetRequestClass(service_method))
                    ret.append((http_path, handler, [endpoint.method]))
        return ret

    return get_service_endpoints(RestApi)


async def _get_request_json(aiohttp_request):
    return await aiohttp_request.json()


async def _get_request_message(request_message, aiohttp_request):
    request_json = await _get_request_json(aiohttp_request)

    # Older clients may post their JSON double-encoded as strings, so the get_json
    # above actually converts it to a string. Therefore, we check this condition
    # (which we can tell for sure because any proper request should be a dictionary),
    # and decode it a second time.
    if isinstance(request_json, six.string_types):
        request_json = json.loads(request_json)

    # If request doesn't have json body then assume it's empty.
    if request_json is None:
        request_json = {}
    parse_dict(request_json, request_message)
    return request_message


def _get_route_info(request_message, aiohttp_request):
    import json
    req = aiohttp_request.path_params
    parse_dict(req, request_message)
    return request_message


def catch_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            response = Response(media_type='application/json',
                                status_code=500,
                                content="Error")
            # status_code=e.g
            # response.set_data(e.serialize_as_json())
            # response.status_code = e.get_http_status_code()
            return response
    return wrapper


@catch_exception
async def _get_item(request: Request):
    request_message = _get_route_info(GetItem(), request)
    # Eg: You can access to request_message field id for ex
    response_message = GetItem.Response()
    response_message.item.id = '1'
    response_message.item.msg = 'foo'
    return Response(content=message_to_json(response_message),
                    media_type='application/json')


def GetItemsModel_to_GetItem(result):
    return Item(id=result.id, msg=result.msg)


@catch_exception
async def _get_items(request: Request):
    request_message = _get_route_info(GetItems(), request)
    # Eg: You can access to request_message field id for ex
    response_message = GetItems.Response()
    response_message.items.extend(
        [Item(id='1', msg='foo'), Item(id='2', msg='foo')])
    return Response(content=message_to_json(response_message),
                    media_type='application/json')


@catch_exception
async def _post_item(request: Request):
    request_message = await _get_request_message(PostItem(), request)
    # Eg: Store here the item inside your DB ...
    response_message = PostItem.Response()
    response_message.item.id = '1'
    response_message.item.msg = request_message.item.msg
    return Response(content=message_to_json(response_message),
                    media_type='application/json')

HANDLERS = {
    # Tracking Server APIs
    GetItem: _get_item,
    GetItems: _get_items,
    PostItem: _post_item
}
