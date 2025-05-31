from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route("/users", methods=['GET'], strict_slashes=False)
def all():
    users = storage.all()
    all_user = {}
    for user in users:
        all_user.append(user)
    return jsonify(all_user.to_dict()), 200

@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Get user by id"""
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    return jsonify(users.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user"""
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creating a user"""
    user_data = request.get_json()

    if not user_data:
        abort(400, "Not a JSON")

    if 'email' not in user_data:
        abort(400, "Missing email")

    if 'password' not in user_data:
        abort(400, "Missing password")

    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict())

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updating the users data"""
    users = storage.get(User, user_id)
    if not users:
        abort(404)

    user_data = request.get_json()
    if not user_data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user_data.items():
        if key not in ignore_keys:
            setattr(users, key, value)

    return jsonify(user_data.to_dict()), 200
    

