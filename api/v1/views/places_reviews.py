#!/usr/bin/python3
"""
create a new view for Review objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'], strict_slashes=False)
def places_place_id_reviews(place_id):
    """
    Methods:
        GET: Retrieves the list of all Review objects of a Place
        POST: Creates a Review
    """
    if storage.get("Place", place_id) is None:
        abort(404)

    # GET method
    if request.method == 'GET':
        reviewList = []

        reviews = storage.all('Review')
        for review in reviews.values():
            reviewsDict = review.to_dict()
            if reviewsDict['place_id'] == place_id:
                reviewList.append(reviewsDict)

        return jsonify(reviewList)

    # POST method
    elif request.method == 'POST':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        if "user_id" not in requestDict:
            abort(400, 'Missing user_id')

        if storage.get("User", requestDict["user_id"]) is None:
            abort(404)

        if "text" not in requestDict:
            abort(400, 'Missing text')

        requestDict['place_id'] = place_id
        new_review = Review(**requestDict)
        storage.new(new_review)
        storage.save()
        return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def reviews_review_id(review_id):
    """
    Methods:
        GET: Retrieves a Review object
        DELETE: Deletes a Review object
        PUT: Updates a Review object
    """
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    # GET method
    if request.method == 'GET':
        return review.to_dict()

    # DELETE method
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return {}, 200

    # PUT method
    if request.method == 'PUT':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        ignoredList = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, value in requestDict.items():
            if key not in ignoredList:
                setattr(review, key, value)

        review.save()
        return review.to_dict(), 200
