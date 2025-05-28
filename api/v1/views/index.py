#!/usr/bin/python
from api.v1.views import app_views
from flask import jsonify
@app_views.route('/status')
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})