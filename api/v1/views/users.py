#!/usr/bin/python3
"""users view module"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """handles /users route"""
    if request.method == 'GET':
        users_obj = storage.all('User')
        users_obj = [obj.to_dict() for obj in users_obj.values()]
        return jsonify(users_obj)
    if request.method == 'POST':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        if req_body.get('email') is None:
            abort(400, 'Missing email')
        if req_body.get('password') is None:
            abort(400, 'Missing password')
        new_user = User(**req_body)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def a_user(user_id=None):
    """handles /users/<user_id> route"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        user.delete()
        del user
        return jsonify({})
    if request.method == 'PUT':
        req_body = request.get_json()
        if req_body is None:
            abort(400, 'Not a JSON')
        user.update(req_body)
        return jsonify(user.to_dict())
