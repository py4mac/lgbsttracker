import json
import os
import re
import six
from functools import wraps
from aiohttp import web

from lgbsttracker.exceptions import LgbsttrackerException
from lgbsttracker.utils.proto_utils import parse_dict


async def get_request_info(request_message, request):
    request_json = await request.json()

    if isinstance(request_json, six.string_types):
        request_json = json.loads(request_json)

    if request_json is None:
        request_json = {}
    parse_dict(request_json, request_message)
    return request_message


def get_route_info(request_message, request):
    import json

    req = request.match_info
    parse_dict(req, request_message)
    return request_message


def get_args_info(args, key, key_type, default):
    try:
        val = args.get(key, default)
        if val is None:
            return None
        return key_type(val)
    except Exception:
        return default


def catch_lgbsttracker_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LgbsttrackerException as e:
            return web.json_response(text=e.serialize_as_json(), status=e.get_http_status_code())

    return wrapper


def async_catch_lgbsttracker_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except LgbsttrackerException as e:
            return web.json_response(text=e.serialize_as_json(), status=e.get_http_status_code())

    return wrapper
