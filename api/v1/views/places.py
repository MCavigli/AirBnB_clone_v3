#!/usr/bin/python3

'''
Create a new view for City objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from api.v1.views import get, delete, post, put


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def place_crud(city_id=None, place_id=None):
    '''Returns GET, DELETE, PUT, POST methods'''
    data = {
            'str': 'Place',
            '_id': place_id,
            'p_id': city_id,
            'p_prop': 'city_id',
            'p_child': 'places',
            'p_str': 'City',
            'check': ['user_id', 'name'],
            'ignore': ['created_at', 'updated_at', 'id', 'user_id', 'city_id']}
    methods = {
            'GET': get,
            'DELETE': delete,
            'POST': post,
            'PUT': put
            }
    if request.method in methods:
        return methods[request.method](data)
