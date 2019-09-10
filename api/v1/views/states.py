#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, Response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET',
                                                                      'DELETE',
                                                                      'PUT'])
def get_state(state_id=None):
    """  """
    objs = storage.all("State").values()
    if request.method == 'GET':
        obj = []
        if state_id == None:
            for i in objs:
                obj.append(i.to_dict())
            return jsonify(obj)
        else:
            for i in objs:
                if i.id == state_id:
                    return jsonify(i.to_dict())
            abort(404)
    elif request.method == 'DELETE':
        for i in objs:
            if i.id == state_id:
                print("***")
                print(i)
                print("***")
                storage.delete(i)
                #i.delete()
                storage.save()
                return jsonify({}), 200
        abort(404)
    elif request.method == 'POST':
        if not request.content_type == 'application/json':
            return jsonify({'error': 'Not a JSON'}), 400
        req = request.get_json()
        # req == {name: ca}
        if 'name' not in req:
            return jsonify({'error': 'Missing name'}), 400
        new_state = State(**req)
        new_state.save()
        objs = storage.all("State").values()
        for i in objs:
            if i.name == req['name']:
                return jsonify(i.to_dict()), 201
    elif request.method == "PUT":
        if not request.content_type == 'application/json':
            return jsonify({'error': 'Not a JSON'}), 400
        req = request.get_json()
        ignore = ['created_at', 'updated_at', 'id']
        for i in objs:
            if i.id == state_id:
                for k, v in req.items():
                    if k not in ignore:
                        i.k = v
                        storage.save()
                        return jsonify(i.to_dict()), 200
        abort(404)
