#!/usr/bin/python3
"""reviews view module"""
from flask import jsonify, request, abort
from os import getenv
from api.v1.views import app_views
from models import storage


STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_place(place_id=None):
    """handles /places/<place_id>/amenities route"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, 'Not found')
    if STORAGE_TYPE == 'db':
        place_amenities = place.amenities
    else:
        place_amenities_ids = place.amenities
        place_amenities = []
        for id in place_amenities_ids:
            place_amenities.append(storage.get('Amenity', id))
    place_amenities = [obj.to_dict() for obj in place_amenities]
    return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def place_amenity(place_id=None, amenity_id=None):
    """handles /places/<place_id>/amenities/<amenity_id> route"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None:
        abort(404, 'Not found')
    if amenity is None:
        abort(404, 'Not found')

    if request.method == 'POST':
        if amenity in place.amenities or amenity.id in place.amenities:
            return jsonify(amenity.to_dict()), 200
        if STORAGE_TYPE == 'db':
            place.amenities.append(amenity)
        else:
            place.amenities = amenity
        return jsonify(amenity.to_dict()), 201

    if request.method == 'DELETE':
        amenities = place.amenities
        if amenity not in amenities and amenity.id not in amenities:
            abort(404, 'Not found')
        if STORAGE_TYPE == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.pop(amenity.id, None)
        place.save()
        return jsonify({}), 200
