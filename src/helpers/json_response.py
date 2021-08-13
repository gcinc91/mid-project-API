
from flask import request, Response
from bson import json_util
import json


def json_response(data):
    """
    Process data with bson serializer to avoid ObjectID to string errors in flask
    """
    return Response(
        json_util.dumps(data),
        mimetype='application/json'
    )
