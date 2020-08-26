import json
from datetime import datetime, timezone


def to_int(val):
    if val is None:
        return val
    if isinstance(val, str):
        return int(val)

    return val


def iso_datetime_string(timestamp):
    if timestamp is None:
        return None
    if isinstance(timestamp, str):
        timestamp = int(timestamp)

    return datetime.utcfromtimestamp(timestamp / 1000000).strftime('%Y-%m-%d %H:%M:%S')


def json_dumps(obj):
    if obj is None:
        return None
    return json.dumps(obj, separators=(',', ':'))