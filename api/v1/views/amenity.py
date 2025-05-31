#!/usr/bin/python
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all amenities"""
    amenity = storage.all()
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Retrieves an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>')
def delete_amenity(amenity_id):
    """"deleting an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    amenity.save()
    return jsonify({}),200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities():
    """Adds a new amenity"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")

    if 'name' not in amenity_data:
        abort(400, "Missing name")

    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slahes=False)
def update_amenity(amenity_id):
    """Updating an amenity"""
    amenities = storage.get(Amenity, amenity_id)
    amenity_data = request.get_json()
    ignore_key = ['id','created_at','updated_at']
    for key, value in amenity_data.items():
        if key not in ignore_key:
            setattr(amenities,key, value)

