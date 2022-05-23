#!/usr/bin/python3
"""
Create a view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def places_place_id_amenities(place_id):
    """
    Methods:
        GET: Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get("State", place_id)
    if place is None:
        abort(404)

    # GET method
    if request.method == 'GET':
        amenitiesList = []
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            amenitiesObjects = place.amenities
        else:
            amenitiesObjects = place.amenity_ids

        for amenity in amenitiesObjects:
            amenitiesList.append(amenity)

        return jsonify(amenitiesList)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def places_place_id_amenities_amenity_id(place_id, amenity_id):
    """
    Methods:
        DELETE: Deletes a Amenity object to a Place
        POST: Link a Amenity object to a Place
    """
    place = storage.get("State", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenitiesObjects = place.amenities
    else:
        amenitiesObjects = place.amenity_ids

    # DELETE method
    if request.method == 'DELETE':
        if amenity not in amenitiesObjects:
            abort(404)

        storage.delete(amenity)
        storage.save()
        return {}, 200

    # POST method
    if request.method == 'POST':
        if amenity not in amenitiesObjects:
            amenitiesObjects.append(amenity)
            storage.save()

        return amenity.to_dict(), 200
