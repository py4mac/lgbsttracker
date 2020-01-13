import base64
import time
import logging
import json

import requests

from google.api.annotations_pb2 import http
from lgbsttracker.utils.string_utils import strip_suffix


def _get_path(path_prefix, endpoint_path):
    return "{}{}".format(path_prefix, endpoint_path)


def search_endpoints(http_rule):

    """ Return method, path. """
    if http_rule.get != "":
        return ["GET"], http_rule.get
    elif http_rule.put != "":
        return ["PUT"], http_rule.put
    elif http_rule.post != "":
        return ["POST"], http_rule.post
    elif http_rule.delete != "":
        return ["DELETE"], http_rule.delete
    elif http_rule.patch != "":
        return ["PATCH"], http_rule.patch
    return [], None


def extract_api_info_for_service(service, path_prefix):
    """ Return a dictionary mapping each API method to a tuple (path, HTTP method)"""
    service_methods = service.DESCRIPTOR.methods
    res = {}
    for service_method in service_methods:
        http_rule = service_method.GetOptions().Extensions[http]
        method, http_path = search_endpoints(http_rule)
        endpoint_path = _get_path(path_prefix, http_path)
        res[service().GetRequestClass(service_method)] = (endpoint_path, method[0])
    return res
