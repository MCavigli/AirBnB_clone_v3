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
    if request.method == 'GET':
        return get(data)
    elif request.method == 'DELETE':
        return delete(data)
    elif request.method == 'POST':
        return post(data)
    elif request.method == "PUT":
        return put(data)


def get(data):
    if data["_id"] is None:
        objs = storage.all(data["str"]).values()
        _list = []
        for obj in objs:
            _list.append(obj.to_dict())
        return jsonify(_list), 200
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
    if not request.content_type == 'application/json':
        return jsonify({'error': 'Not a JSON'}), 400
    req = request.get_json()
    if 'name' not in req:
        return jsonify({'error': 'Missing name'}), 400
    new = data['cls'](**req)
    new.save()
    objs = storage.all(data['str']).values()
    for obj in objs:
        if obj.name == req['name']:
            return jsonify(obj.to_dict()), 201


def put(data):
    if not request.content_type == 'application/json':
        return jsonify({'error': 'Not a JSON'}), 400
    req = request.get_json()
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

