#!/usr/bin/python3

'''
Create a new view for State objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def states_crud(state_id=None):
    '''Returns GET, DELETE, PUT, POST methods'''
    data = {
            'str': 'State',
            '_id': state_id,
            'p_id': None,
            'check': ['name'],
            'ignore': ['created_at', 'updated_at', 'id']
            }
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)


def get(data):
    if data['p_id']:
        parent = storage.get(data['p_str'], data['p_id'])
        if parent:
            return jsonify([p.to_dict() for p in
                           getattr(parent, data['p_child'])]), 200
        abort(404)
    if data['_id']:
        found = storage.get(data['str'], data['_id'])
        if found:
            return jsonify(found.to_dict()), 200
        abort(404)
    else:
        return jsonify([x.to_dict() for x in
                       storage.all(data['str']).values()]), 200


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
    for c in data['check']:
        if c not in req:
            return jsonify({'error': 'Missing {}'.format(c)}), 400
    if data['p_id']:
        parent = storage.get(data['p_str'], data['p_id'])
        if parent:
            req[data['p_prop']] = data['p_id']
            new = eval(data['str'])(**req)
            new.save()
            return jsonify(new.to_dict()), 201
        abort(404)
    new = eval(data['str'])(**req)
    new.save()
    return jsonify(new.to_dict()), 201


def put(data):
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    found = storage.get(data['str'], data['_id'])
    if found:
        for k, v in req.items():
            if k not in data['ignore']:
                setattr(found, k, v)
        storage.save()
        return jsonify(found.to_dict()), 200
    else:
        abort(404)
