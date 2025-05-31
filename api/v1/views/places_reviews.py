#!/usr/bin/python
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review

@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id):
    """Retrieving a list of all reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all_reviews = []
    for reviews in place.reviews:
        all_reviews.append(reviews)
    return jsonify(all_reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'])
def single_review(review_id):
    """Retrieving a single review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deleting a single review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def creating_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")

    if 'user_id' not in review_data:
        abort(400, "Missing user_id")

    user = storage.get(User, review_data['user_id'])  
    if not user:
        abort(404)  

    if 'text' not in review_data:
        abort(400, "Missing text")

    new_review = Review(**review_data)
    new_review.place_id = place_id
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updating a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    storage.save()

    return jsonify(review.to_dict()), 200
