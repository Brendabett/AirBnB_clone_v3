#!/usr/bin/python3
"""places view module"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, storage_t
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
       retrieves all Place objects depending of the JSON in
       the body of the request
    """
    all_places = [place for place in storage.all('Place').values()]
    req_body = request.get_json()
    if req_body is None:
        abort(400, 'Not a JSON')
    states_list = req_body.get('states')
    cities_list = req_body.get('cities')
    amenities_list = req_body.get('amenities')
    if states_list and len(states_list) > 0:
        all_cities = storage.all('City')
        states = [city.id for city in all_cities.values()
                  if city.state_id in states_list]
        state_cities = set(states)
    else:
        state_cities = set()
    if cities_list and len(cities_list) > 0:
        cities_id = [id for id in cities_list if storage.get('City', id)]
        cities = set(cities_id)
        state_cities = state_cities.union(cities)
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities_list is None or len(amenities_list) == 0:
        result = [place.to_dict() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities_list and len(amenities_list) > 0:
        amen_ids = [id for id in amenities_list if storage.get('Amenity', id)]
        amenities_list = set(amen_ids)
        for place in all_places:
            p_amenities = None
            if storage_t == 'db' and place.amenities:
                p_amenities = [amen.id for amen in place.amenities]
            elif len(place.amenities) > 0:
                p_amenities = place.amenities
            if p_amenities and all([a in p_amenities for a in amenities_list]):
                places_amenities.append(place)
    else:
        places_amenities = all_places
    result = [place.to_dict() for place in places_amenities]
    return jsonify(result)
