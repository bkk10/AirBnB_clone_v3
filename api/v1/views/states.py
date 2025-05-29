#!/usr/bin/python
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all states"""
    all_states = storage.all(State).values()
    state_list = []
    for state in all_states:
        state_list.append(state.to_dict())
    return jsonify(state_list) 

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves the id of a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods = ['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states():
    """return new state with 201, dictionary doesn't 
    have name raise error if http body request is not 
    a valid json raise 400"""
    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")

    if 'name' not in data:
        abort(400, "Missing name")

    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods = ['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state object with the provided JSON data"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
    
    
