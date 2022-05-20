#!/usr/bin/python3
"""
index module witch define an index page
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """returns a JSON: 'status': 'OK'"""
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """
    Return a JSON with the number of instance in the database
    """
    count = storage.count
    return {"amenities": count(Amenity),
            "cities": count(City),
            "places": count(Place),
            "reviews": count(Review),
            "states": count(State),
            "users": count(User)}
