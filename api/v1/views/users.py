#!/usr/bin/python3
"""
view for User objects that handles all default RESTFul API actions:

    *   Retrieves the list of all User objects: GET /api/v1/users
    *   Retrieves a User object: GET /api/v1/users/<user_id>
    *   Deletes a User object:: DELETE /api/v1/users/<user_id>
    *   Creates a User: POST /api/v1/users
    *   Updates a User object: PUT /api/v1/users/<user_id>
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request, jsonify


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """
    Method GET:
        Retrieves the list of all User objects
    Method Post:
        Returns the new User with the status code 201
    """
    # GET method
    if request.method == 'GET':
        all_users = storage.all(User)
        users_json = []
        for key, value in all_users.items():
            users_json.append(value.to_dict())
        return jsonify(users_json)

    # POST method
    elif request.method == 'POST':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        if 'email' not in requestDict:
            abort(400, 'Missing email')

        if 'password' not in requestDict:
            abort(400, 'Missing password')

        new_state = User(**requestDict)
        storage.new(new_state)
        storage.save()
        return new_state.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_id(user_id):
    """
    Method that searching by id, a user.

    If the user_id doesn't exist:
        abort a 404 page error.

    GET method:
        Return the dictionnary representation of the user catch

    DELETE method:
        Delete the user catches and return an empty dictionnary
    """
    user_catch = storage.get(User, user_id)

    if user_catch is None:
        abort(404)

    # Method request GET, return dict representation of user
    if request.method == 'GET':
        return user_catch.to_dict()

    # Method request DELETE, return empty user
    if request.method == 'DELETE':
        storage.delete(user_catch)
        storage.save()
        return {}, 200

    # Method request PUT
    if request.method == 'PUT':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        invalid_key = ['id', 'email', 'created_at', 'updated_at']
        for key, value in requestDict.items():
            if key not in invalid_key:
                setattr(user_catch, key, value)

        user_catch.save()
        return user_catch.to_dict(), 200
