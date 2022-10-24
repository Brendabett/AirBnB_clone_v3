#!/usr/bin/python3
"""module for the api endpoint"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def handle_teardown(exception):
    """Removes current session in sqlalchemy"""
    storage.close()


@app.errorhandler(404)
def hadle_404_error(ex):
    """handles the 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
