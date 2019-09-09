#!/usr/bin/python3

"""
Create a new view for State objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def crud(state_id=None):
    """Returns GET, DELETE, PUT, POST methods"""
    data = {"cls": State, "str": "State", "_id": state_id}
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)


def get(data):
    if data["_id"] is None:
        return jsonify([x.to_dict() for x in
                       storage.all(data["str"]).values()]), 200
    else:
        found = storage.get(data["str"], data["_id"])
        if found:
            return jsonify(found.to_dict()), 200
        abort(404)


def delete(data):
    found = storage.get(data['str'], data['_id'])
    if found:
        storage.delete(found)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


def post(data):
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in req:
        return jsonify({'error': 'Missing name'}), 400
    new = data['cls'](**req)
    new.save()
    return jsonify(new.to_dict()), 201


def put(data):
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    ignore = ['created_at', 'updated_at', 'id']
    found = storage.get(data['str'], data['_id'])
    if found:
        for k, v in req.items():
            if k not in ignore:
                setattr(found, k, v)
        storage.save()
        return jsonify(found.to_dict()), 200
    else:
        abort(404)
