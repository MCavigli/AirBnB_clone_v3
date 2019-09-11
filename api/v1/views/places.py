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


@app_views.route('/places_search',
                 strict_slashes=False,
                 methods=['POST'])
def search_crud():
    ''' '''
    from models import storage
    print("here")
    req = request.get_json()
    if req is None:
        return jsonify({'error': 'Not a JSON'}), 400
    val = storage.all("Place").values()
    if req == {}:
        return jsonify([x.to_dict() for x in val]), 200
    if all(x == 0 for x in [len(v) for k, v in req.items()]):
        return jsonify([x.to_dict() for x in val]), 200
    state_list = []
    for s_id in req['states']:
        found = storage.get("State", s_id)
        if found:
            state_list.append(found)
    city_list = []
    for state in state_list:
        city_list.extend(state.cities)
    for c_id in req['cities']:
        found = storage.get("City", c_id)
        if found and found not in city_list:
            city_list.append(found)
    places = []
    for cities in city_list:
        places.extend(cities.places)
    if not hasattr(req, 'amenities') or req['amenities'] == []:
        return jsonify([x.to_dict() for x in places]), 200
    amenity_list = []
    result = []
    for a_id in req['amenities']:
        found = storage.get("Amenity", a_id)
        if found:
            amenity_list.append(found)
    for place in places:
        for amenity in amenity_list:
            if amenity not in place.amenities:
                break
        result.append(place)
#        if len(place.amenities) == len(amenity_list):

    return jsonify([x.to_dict() for x in result]), 200
