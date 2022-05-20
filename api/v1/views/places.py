#!/usr/bin/python3
"""
Create a new view for Place objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def cities_city_id_places(city_id):
    """
    Methods:
        GET: Retrieves the list of all Place objects of a City
        POST: Creates a Place
    """
    if storage.get("City", city_id) is None:
        abort(404)

    # GET method
    if request.method == 'GET':
        placesList = []

        places = storage.all('Place')
        for place in places.values():
            placesDict = place.to_dict()
            if placesDict['city_id'] == city_id:
                placesList.append(placesDict)

        return jsonify(placesList)

    # POST method
    elif request.method == 'POST':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        if not "user_id" in requestDict:
            abort(400, 'Missing user_id')
        
        user = storage.get("User", requestDict["user_id"])
        if user is None:
            abort(400)

        if "name" not in requestDict:
            abort(400, 'Missing name')

        requestDict['city_id'] = city_id
        newPlace = Place(**requestDict)
        storage.new(newPlace)
        storage.save()
        return newPlace.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_place_id(place_id):
    """
    Methods:
        GET: Retrieves a Place object
        DELETE: Deletes a Place object
        PUT: Updates a Place object
    """
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    # GET method
    if request.method == 'GET':
        return place.to_dict()

    # DELETE method
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return {}, 200

    # PUT method
    if request.method == 'PUT':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        ignoredList = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, value in requestDict.items():
            if key not in ignoredList:
                setattr(place, key, value)

        return place.to_dict(), 200
