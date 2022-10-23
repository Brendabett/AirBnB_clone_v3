#!/usr/bin/python3
"""amenities view module"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """handles /amenities route"""
    if request.method == 'GET':
        amenities_obj = storage.all('Amenity')
        amenities_obj = [obj.to_dict() for obj in amenities_obj.values()]
        return jsonify(amenities_obj)
    if request.method == 'POST':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        if req_body.get('name') is None:
            abort(400, 'Missing name')
        new_amenity = Amenity(**req_body)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def fun_amenity(amenity_id=None):
    """handles /amenities/<amenity_id> route"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        amenity.delete()
        del amenity
        return jsonify({})
    if request.method == 'PUT':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        amenity.update(req_body)
        return jsonify(amenity.to_dict())
