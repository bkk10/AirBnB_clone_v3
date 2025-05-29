from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, request, abort


@app_views.route('states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_city_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/Cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """Retrieves a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """Deleting a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def new_city(state_id):
    """Returns a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        city_data = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    if not city_data:
        abort(400, "Not a JSON")
    
    if 'name' not in city_data:
        abort(400, "Missing name")

    city_data['state_id'] = state_id
    new_city = City(**city_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updating a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city_name = request.get_json()
    if not city_name:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in city_name.items():
        if key not in ignore_keys:
            setattr(City, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200


