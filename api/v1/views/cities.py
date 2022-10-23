#!/usr/bin/python3
"""cities view module"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id=None):
    """handles /states/<state_id>/cities route"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        cities_obj = storage.all('City')
        cities_obj = [obj.to_dict() for obj in cities_obj.values()
                      if obj.state_id == state_id]
        return jsonify(cities_obj)
    if request.method == 'POST':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        if req_body.get('name') is None:
            abort(400, 'Missing name')
        req_body['state_id'] = state_id
        new_city = City(**req_body)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def a_city(city_id=None):
    """handles /cities/<city_id> route"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        city.delete()
        del city
        return jsonify({})
    if request.method == 'PUT':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        city.update(req_body)
        return jsonify(city.to_dict())
