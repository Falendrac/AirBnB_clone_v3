#!/usr/bin/python3
"""
create a new view for City objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """
    Methods:
        GET: Retrieves the list of all Amenity objects
        POST: Creates a Amenity
    """
    # GET method
    if request.method == 'GET':
        amenitiesList = []
        amenities = storage.all('Amenity')

        for amenity in amenities.values():
            amenitiesList.append(amenity.to_dict())

        return jsonify(amenitiesList)

    # POST method
    elif request.method == 'POST':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        if "name" not in requestDict:
            abort(400, 'Missing name')

        newAmenity = Amenity(**requestDict)
        storage.new(newAmenity)
        storage.save()

        return newAmenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_amenity_id(amenity_id):
    """
    Methods:
        GET: Retrieves a Amenity object
        DELETE: Deletes a Amenity object
        PUT: Updates a Amenity object
    """
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    # GET method
    if request.method == 'GET':
        return amenity.to_dict()

    # DELETE method
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return {}, 200

    # PUT method
    if request.method == 'PUT':
        requestDict = request.get_json()

        if not requestDict:
            return 'Not a JSON', 400

        ignoredList = ["id", "created_at", "updated_at"]
        for key, value in requestDict.items():
            if key not in ignoredList:
                setattr(amenity, key, value)

        amenity.save()
        return amenity.to_dict(), 200
