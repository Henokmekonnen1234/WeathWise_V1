#!/usr/bin/env python3
"""
transaction.py

This module defines API endpoints related to user registration, login, user profile management,
and user deletion for the WealthWise application.

It uses Flask and Flask-JWT-Extended for authentication, SQLAlchemy for database operations,
and custom utility functions for validation, encryption, and error handling.

Attributes:
    app_views (Blueprint): Blueprint for organizing API routes.
    request (Request): Object for handling HTTP requests in Flask.
    jsonify (Function): Function for converting Python dictionaries to JSON responses.
    create_access_token (Function): Generates JWT access tokens for authentication.
    jwt_required (Decorator): Validates JWT tokens for protected routes.
    get_jwt_identity (Function): Retrieves the identity (user ID) from a JWT token.
    storage (SQLAlchemy): Database storage for ORM operations.
    User (Class): SQLAlchemy model for User data.
    taken_value (Function): Checks if a value is already taken in the database.
    encrypt (Function): Encrypts passwords for secure storage.
    decrypt (Function): Decrypts passwords for authentication.
    not_found (dict): Dictionary with a "Not Found" message for error responses.
    is_user_valid (Function): Validates user data before registration or update.

Functions:
    user_register: Endpoint for user registration.
    login: Endpoint for user login authentication.
    get_user: Endpoint to retrieve user profile information.
    update_user: Endpoint to update user profile information.
    delete_user: Endpoint to delete user account.

Example:
    localhost:5000/api/v1/login
"""

from api.v1.views import app_views
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from models import storage
from models.user import User
from models.utility import taken_value, encrypt, decrypt, not_found
from models.utility import is_user_valid

@app_views.route("/register", methods=["POST"], strict_slashes=False)
@swag_from("documentation/user/register.yml")
def user_register():
    """
    Endpoint for user registration.

    Validates user data, checks for existing usernames,
    encrypts the password, creates a new User object, and saves it to the database.

    Returns:
        JSON: JSON response with user data including the newly created user ID.
              If validation fails or username is taken, returns an error message.
    """
    user_data = request.get_json()
    if is_user_valid(user_data):
        return jsonify(is_user_valid(user_data)), 400
    if taken_value(User, **user_data):
        return jsonify(taken_value(User, **user_data)), 409
    user_data["password"] = encrypt(user_data["password"])
    user = User(**user_data)
    user.save()
    return jsonify(user.to_dict())


@app_views.route("/login", methods=["POST"], strict_slashes=False)
@swag_from("documentation/user/login.yml")
def login():
    """
    Endpoint for user login authentication.

    Retrieves login data, validates username, checks password, and generates a JWT token if successful.

    Returns:
        JSON: JSON response with a JWT token if login is successful.
              Returns error messages for incorrect username or password, or if data is missing.
    """
    login_data = request.get_json()
    if login_data:
        user = storage.filter(User, "username", login_data["username"])
        if user:
            if decrypt(login_data["password"], user.password):
                token = create_access_token(identity=str(user._id))
                return jsonify({"token": token})
            else:
                return jsonify("Password is not correct"), 401
        else:
            return jsonify("Username is not found"), 404
    else:
        return jsonify("Data not found"), 404


@app_views.route("/user", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from("documentation/user/get_user.yml")
def get_user():
    """
    Endpoint to retrieve user profile information.

    Requires a valid JWT token for authentication.

    Returns:
        JSON: JSON response with user profile information.
              Returns a "Not Found" message if user does not exist.
    """
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    user._id = str(user._id)
    return jsonify(user.to_dict())


@app_views.route("/user", methods=["PUT"], strict_slashes=False)
@jwt_required()
@swag_from("documentation/user/update_user.yml")
def update_user():
    """
    Endpoint to update user profile information.

    Requires a valid JWT token for authentication.
    Validates user data, updates user information, and saves changes to the database.

    Returns:
        JSON: JSON response with updated user profile information.
              Returns validation errors if user data is invalid.
    """
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    user_data = request.get_json()
    if is_user_valid(user_data):
        return jsonify(is_user_valid(user_data)), 400
    for key, value in user_data.items():
        setattr(user, key, value)
    user.update()
    return jsonify(user.to_dict())


@app_views.route("/user", methods=["DELETE"], strict_slashes=False)
@jwt_required()
@swag_from("documentation/user/delete_user.yml")
def delete_user():
    """
    Endpoint to delete user account.

    Requires a valid JWT token for authentication.
    Deletes user from the database.

    Returns:
        JSON: JSON response with user's full name after deletion.
              Returns an error if user does not exist.
    """
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    user_name = f"{user.first_name} {user.last_name}"
    if not user:
        return jsonify(not_found), 400
    user.delete()
    return jsonify(user_name)
