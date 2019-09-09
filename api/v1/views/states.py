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
def get_state(state_id=None):
    """Returns GET, DELETE, PUT, POST methods"""
    if request.method == 'GET':
        if state_id is None:
            objs = storage.all("State").values()
            _list = []
            for obj in objs:
                _list.append(obj.to_dict())
            return jsonify(_list), 200
        else:
            state = storage.get("State", state_id)
            if state:
                return jsonify(state.to_dict()), 200
            abort(404)
    elif request.method == 'DELETE':
        state = storage.get("State", state_id)
        if state:
            storage.delete(state)
            storage.save()
            storage.reload()
            return jsonify({}), 200
        else:
            abort(404)
    elif request.method == 'POST':
        if not request.content_type == 'application/json':
            return jsonify({'error': 'Not a JSON'}), 400
        req = request.get_json()
        if 'name' not in req:
            return jsonify({'error': 'Missing name'}), 400
        new_state = State(**req)
        new_state.save()
        objs = storage.all("State").values()
        for obj in objs:
            if obj.name == req['name']:
                return jsonify(obj.to_dict()), 201
    elif request.method == "PUT":
        if not request.content_type == 'application/json':
            return jsonify({'error': 'Not a JSON'}), 400
        req = request.get_json()
        ignore = ['created_at', 'updated_at', 'id']
        state = storage.get("State", state_id)
        if state:
            for k, v in req.items():
                if k not in ignore:
                    setattr(state, k, v)
                    storage.save()
                    storage.reload()
                    return jsonify(state.to_dict()), 200
        abort(404)
