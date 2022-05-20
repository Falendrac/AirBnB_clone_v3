#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions:

    *   Retrieves the list of all State objects: GET /api/v1/states
    *   Retrieves a State object: GET /api/v1/states/<state_id>
    *   Deletes a State object:: DELETE /api/v1/states/<state_id>
    *   Creates a State: POST /api/v1/states
    *   Updates a State object: PUT /api/v1/states/<state_id>
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """
    Method GET:
        Retrieves the list of all State objects
    Method Post:
        Returns the new State with the status code 201
    """
    # GET method
    if request.method == 'GET':
        all_states = storage.all(State)
        states_json = []
        for key, value in all_states.items():
            states_json.append(value.to_dict())
        return jsonify(states_json)

    # POST method
    elif request.method == 'POST':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        if 'name' not in requestDict:
            abort(400, 'Missing name')

        new_state = State(**requestDict)
        storage.new(new_state)
        storage.save()
        return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state_id(state_id):
    """
    Method that searching by id, a state.

    If the state_id doesn't exist:
        abort a 404 page error.

    GET method:
        Return the dictionnary representation of the state catch

    DELETE method:
        Delete the state catches and return an empty dictionnary
    """
    state_catch = storage.get(State, state_id)

    if state_catch is None:
        abort(404)

    # Method request GET, return dict representation of state
    if request.method == 'GET':
        return state_catch.to_dict()

    # Method request DELETE, return empty state
    if request.method == 'DELETE':
        storage.delete(state_catch)
        storage.save()
        return {}, 200

    # Method request PUT
    if request.method == 'PUT':
        requestDict = request.get_json()

        if not requestDict:
            abort(404, 'Not a JSON')

        invalid_key = ['id', 'created_at', 'updated_at']
        for key, value in requestDict.items():
            if key not in invalid_key:
                setattr(state_catch, key, value)
        return state_catch.to_dict(), 200
