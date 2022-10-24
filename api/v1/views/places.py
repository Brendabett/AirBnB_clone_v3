#!/usr/bin/python3
"""places view module"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id=None):
    """handles /cities/<city_id>/places route"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        places_obj = storage.all('Place')
        places_obj = [obj.to_dict() for obj in places_obj.values()
                      if obj.city_id == city_id]
        return jsonify(places_obj)
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
        if req_body.get('name') is None:
            abort(400, 'Missing name')
        req_body['city_id'] = city_id
        new_place = Place(**req_body)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def a_place(place_id=None):
    """handles /places/<place_id> route"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        place.delete()
        del place
        return jsonify({})
    if request.method == 'PUT':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        place.update(req_body)
        return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
        retrieves all Place objects depending of the JSON in the body
        of the request
    """
    params = request.get_json()
    if type(params) != dict:
        abort(400, 'Not a JSON')
    id_states = params.get('states', [])
    id_cities = params.get('cities', [])
    id_amenities = params.get('amenities', [])
    if id_states == id_cities == []:
        places = storage.all('Place').values()
    else:
        states = [
            storage.get('State', id) for id in id_states
            if storage.get('State', id)
        ]
        cities = [city for state in states for city in state.cities]
        cities += [
            storage.get('City', id) for id in id_cities
            if storage.get('City', id)
        ]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]
    amenities = [
        storage.get('Amenity', id) for id in id_amenities if
        storage.get('Amenity', id)
    ]
    confirmed_places = []
    for place in places:
        confirmed_places.append(place.to_dict())
        for amenity in amenities:
            if amenity not in place.amenities:
                confirmed_places.pop()
                break
    return jsonify(confirmed_places)
