# Database schema
from bson import ObjectId
from flask import json

json_user_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "lat": {"type": "number"},
        "lon": {"type": "number"}
    },
    "required": ["first_name", "last_name", "lat", "lon"]
}

json_put_user_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": ["string", "null"]},
        "last_name": {"type": ["string", "null"]},
        "lat": {"type": "number"},
        "lon": {"type": "number"}
    },
    "required": ["first_name", "last_name"]
}

json_client_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "password"]
}


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
