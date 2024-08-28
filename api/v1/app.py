#!/usr/bin/env python3
"""
app.py

This module initializes a Flask application for the WealthWise API.

It sets up the Flask app with necessary configurations, middleware, error handling,
and database connections using SQLAlchemy and Flask extensions.

Usage:
    Run this module to start the Flask application.

Attributes:
    app (Flask): The main Flask application instance.
    app_views (Blueprint): Blueprint for organizing API routes.
    cors (CORS): Cross-Origin Resource Sharing configuration for Flask app.
    jwt (JWTManager): JWT token management for authentication.
    storage (SQLAlchemy): Database storage for ORM operations.
    CACHE_TYPE (str): Type of caching mechanism used in the application.

Functions:
    open_mongodb: Function to reload MongoDB connections before each request.
    close_mongodb: Function to close MongoDB connections after each request.
    error_handler: Error handler function to manage 404 errors with JSON response.

Example:
    $ python app.py
"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from models import storage
from uuid import uuid4

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["SECRET_KEY"] = str(uuid4())
app.config['SWAGGER'] = {
    'title': 'WealthWise Restful API',
    'version': 1
}
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*/": {"origins": "*"}})
jwt = JWTManager(app)
swagger = Swagger(app)


@app.route('/documentation/<path:filename>')
def serve_documentation(filename):
    return send_from_directory('documentation', filename)


@app.before_request
def open_mongodb():
    """Reload MongoDB connections before each request."""
    storage.reload()

@app.teardown_appcontext
def close_mongodb(error):
    """Close MongoDB connections after each request."""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """Handle 404 Not Found errors with a JSON response."""
    return make_response(jsonify({'error': f"{error}"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
