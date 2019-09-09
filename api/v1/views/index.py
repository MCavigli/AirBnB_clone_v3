#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'])
def json_ret():
    """ returns a JSON string on an object """
    return jsonify({"status": "OK"})
