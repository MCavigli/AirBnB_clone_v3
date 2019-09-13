#!/usr/bin/python3

'''
Create a new view for City objects that handles
all default RestFul API actions.
'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from api.v1.views import get, delete, post, put
from models import storage
import os


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


@app_views.route('/places_search',
                 strict_slashes=False,
                 methods=['POST'])
def search_crud():
    ''' Filters places by state, city, and amenities '''
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    all_places = storage.all("Place").values()
    if req == {}:
        return jsonify([x.to_dict() for x in all_places]), 200
    if all(x == 0 for x in [len(v) for k, v in req.items()]):
        return jsonify([x.to_dict() for x in all_places]), 200
    state_list = get(req, 'states', 'State')
    print([s.name for s in state_list])
    city_list = set()
    for state in state_list:
        for city in state.cities:
            city_list.add(city)
    cities = req.get('cities')
    if cities:
        for c_id in req['cities']:
            found = storage.get("City", c_id)
            if found:
                city_list.add(found)
    place_list = set()
    for city in city_list:
        for places in city.places:
            place_list.add(places)
    if len(city_list) == 0:
        place_list = all_places
    if not req.get('amenities') or len(req['amenities']) == 0:
        return jsonify([x.to_dict() for x in place_list]), 200
    amenity_list = set()
    result = []
    for a_id in req['amenities']:
        found = storage.get("Amenity", a_id)
        if found:
            amenity_list.add(found.id)
    for place in place_list:
        required_amens = [a.id for a in place.amenities]
        if required_amens and all([x in required_amens for x in amenity_list]):
            result.append(place.id)
    final = [storage.get("Place", x) for x in result]
    super_final = []
    for f in final:
        d = f.to_dict()
        del d['amenities']
        super_final.append(d)
    return jsonify([x for x in super_final]), 200


def get(req, cls_str, cls, id_only=False):
    ''' '''
    _set = set()
    cls_array = req.get(cls_str)
    if cls_array:
        for _id in cls_array:
            found = storage.get(cls, _id)
            if id_only:
                _set.add(found.id)
            elif found:
                _set.add(found)
    return _set


def populate(parent_list, child_prop):
    ''' '''
    _set = set()
    for p in parent_list:
        for child in getattr(p, child_prop):
            _set.add(child)
    return _set
