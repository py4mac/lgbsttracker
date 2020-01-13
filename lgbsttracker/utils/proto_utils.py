import datetime
from google.protobuf.json_format import MessageToJson, ParseDict
from google.protobuf.timestamp_pb2 import Timestamp
from lgbsttracker.utils.date_utils import datetime_to_seconds


def message_to_json(message):
    """Converts a message to JSON, using snake_case for field names."""
    return MessageToJson(message, preserving_proto_field_name=True)


def parse_dict(js_dict, message):
    """Parses a JSON dictionary into a message proto, ignoring unknown fields in the JSON."""
    ParseDict(js_dict=js_dict, message=message, ignore_unknown_fields=True)


def timestamp_to_datetime(ts):
    return datetime.datetime.fromtimestamp(ts.seconds)


def datetime_to_timestamp(dt):
    timestamp = Timestamp()
    timestamp.seconds = datetime_to_seconds(dt)
    return timestamp
