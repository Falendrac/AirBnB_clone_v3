#!/usr/bin/python3
"""
create a new view for City objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def states_state_id_cities(state_id):
    """
    Methods:
        GET: Retrieves the list of all City objects of a State
        POST: Creates a City
    """
    if storage.get("State", state_id) is None:
        abort(404)

    # GET method
    if request.method == 'GET':
        citiesList = []

        cities = storage.all('City')
        for city in cities.values():
            citiesDict = city.to_dict()
            if citiesDict['state_id'] == state_id:
                citiesList.append(citiesDict)

        return jsonify(citiesList)

    # POST method
    elif request.method == 'POST':
        requestDict = request.get_json()

        if not requestDict:
            return 'Not a JSON', 400

        if "name" not in requestDict:
            return 'Missing name', 400

        requestDict['state_id'] = state_id
        newCity = City(**requestDict)
        storage.new(newCity)
        storage.save()
        return newCity.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities_city_id(city_id):
    """
    Methods:
        GET: Retrieves a City object
        DELETE: Deletes a City object
        PUT: Updates a City object
    """
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    # GET method
    if request.method == 'GET':
        return city.to_dict()

    # DELETE method
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return {}, 200

    # PUT method
    if request.method == 'PUT':
        requestDict = request.get_json()

        if not requestDict:
            return 'Not a JSON', 400

        ignoredList = ["id", "state_id", "created_at", "updated_at"]
        for key, value in requestDict.items():
            if key not in ignoredList:
                setattr(city, key, value)

        city.save()
        return city.to_dict(), 200
