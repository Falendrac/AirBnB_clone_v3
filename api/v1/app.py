#!/usr/bin/python3
"""
app module witch define an app
"""

from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={
    "/*": {
        "origins": "0.0.0.0"
    }
})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    """handler for 404 errors"""
    return {"error": "Not found"}, 404


def main():
    """run the Flask server"""
    if os.environ["HBNB_API_HOST"] is None:
        os.environ["HBNB_API_HOST"] = "0.0.0.0"
    if os.environ["HBNB_API_PORT"] is None:
        os.environ["HBNB_API_PORT"] = "5000"

    app.run(
        os.environ["HBNB_API_HOST"],
        port=os.environ["HBNB_API_PORT"],
        threaded=True
    )


if __name__ == '__main__':
    main()
