#!/usr/bin/python3
"""reviews view module"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id=None):
    """handles /places/<place_id>/reviews route"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        reviews_obj = storage.all('Review')
        reviews_obj = [obj.to_dict() for obj in reviews_obj.values()
                       if obj.place_id == place_id]
        return jsonify(reviews_obj)
    if request.method == 'POST':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        user_id = req_body.get('user_id')
        if user_id is None:
            abort(400, 'Missing user_id')
        user = storage.get('User', user_id)
        if user is None:
            abort(404, 'Not found')
        if req_body.get('text') is None:
            abort(400, 'Missing Text')
        req_body['place_id'] = place_id
        new_review = Review(**req_body)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def a_review(review_id=None):
    """handles /reviews/<review_id> route"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        review.delete()
        del review
        return jsonify({}), 200
    if request.method == 'PUT':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        review.update(req_body)
        return jsonify(review.to_dict()), 200
