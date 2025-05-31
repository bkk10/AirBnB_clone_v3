#!/usr/bin/python
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all place objects of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    all_city = []
    for cities in city.places:
        all_city.append(cities)

    return jsonify(all_city)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a single place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new user"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")

    if 'user_id' not in place_data:
        abort(400, "Missing user_id")

    user = storage.get(User, place_data['user_id'])
    if not user:
        abort(404)

    if 'name' not in place_data:
        abort(400, "missing name")

    new_place = Place(**place_data)
    new_place.save()
    return jsonify(new_place.to_dict())

@app_views.route('/places/<place_id>', methods=['PUT'])
def updating_place(place_id):
    """Updating a place id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")

    ignore_keys=['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in place_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict())
