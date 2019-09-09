#!/usr/bin/python3

"""
Create a new view for City objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import City


@app_views.route('/cities/<cities_id>',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def crud(state_id=None):
    """Returns GET, DELETE, PUT, POST methods"""
    pass
