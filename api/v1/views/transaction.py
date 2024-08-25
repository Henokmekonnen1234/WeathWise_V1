#!/usr/bin/env python3
"""
transaction.py

This module defines API endpoints related to transaction management and summaries
for the WealthWise application.

Attributes:
    app_views (Blueprint): Blueprint for organizing API routes.
    request (Request): Object for handling HTTP requests in Flask.
    jsonify (Function): Function for converting Python dictionaries to JSON responses.
    jwt_required (Decorator): Validates JWT tokens for protected routes.
    get_jwt_identity (Function): Retrieves the identity (user ID) from a JWT token.
    storage (SQLAlchemy): Database storage for ORM operations.
    User (Class): SQLAlchemy model for User data.
    Transaction (Class): SQLAlchemy model for Transaction data.
    not_found (dict): Dictionary with a "Not Found" message for error responses.

Functions:
    add_transaction: Endpoint to add a new transaction for a user.
    get_all_transaction: Endpoint to retrieve all transactions for a user with pagination.
    get_transaction: Endpoint to retrieve a specific transaction by ID for a user.
    update_transaction: Endpoint to update a specific transaction by ID for a user.
    txn_summary: Endpoint to retrieve transaction summaries based on year and month for a user.

Example:
    localhost:5000/api/v1/transactions
"""

from api.v1.views import app_views
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from models import storage
from models.user import User
from models.transaction import Transaction
from models.utility import not_found

@app_views.route("/transactions", methods=["POST"], strict_slashes=False)
@jwt_required()
@swag_from('documentation/transaction/add_transaction.yml')
def add_transaction():
    """
    Endpoint to add a new transaction for a user.

    Validates user existence, incoming JSON data, creates a new Transaction object,
    saves it to the database, and updates the user's transaction list.

    Returns:
        JSON: JSON response with the newly created transaction details.
              Returns error messages for validation failures or missing data.
    """
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    txn_data = request.get_json()
    if not txn_data:
        return jsonify(not_found), 404
    transaction = Transaction(**txn_data)
    if not transaction:
        return jsonify(not_found), 404
    transaction.save()
    user.transactions.append(transaction._id)
    user.update()
    return jsonify(transaction.to_dict())

@app_views.route("/transactions", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from('documentation/transaction/get_all_transaction.yml')
def get_all_transaction():
    """
    Endpoint to retrieve all transactions for a user with pagination.

    Retrieves user identity, validates user existence, and retrieves all transactions
    associated with the user, paginated based on provided query parameters.

    Returns:
        JSON: JSON response with paginated transaction data.
              Returns error messages if user is not found or if data retrieval fails.
    """
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    all_txn = storage.filter_all(user, page, page_size)
    return jsonify(all_txn)

@app_views.route("/transactions/<id>", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from('documentation/transaction/get_transaction.yml')
def get_transaction(id=None):
    """
    Endpoint to retrieve a specific transaction by ID for a user.

    Retrieves user identity, validates user existence, retrieves the transaction by ID,
    and verifies if the transaction belongs to the user.

    Returns:
        JSON: JSON response with transaction details if found.
              Returns "Not Found" message if transaction or user is not found.
    """
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    if not id:
        return jsonify(not_found), 404
    transaction = storage.get(Transaction, id)
    if not transaction:
        return jsonify(not_found), 404
    if transaction._id in user.transactions:
        return jsonify(transaction.to_dict())
    else:
        return jsonify(not_found), 404

@app_views.route("/transactions/<id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
@swag_from('documentation/transaction/update_transaction.yml')
def update_transaction(id=None):
    """
    Endpoint to update a specific transaction by ID for a user.

    Retrieves user identity, validates user existence, retrieves the transaction by ID,
    updates the transaction with incoming JSON data, and saves changes to the database.

    Returns:
        JSON: JSON response with updated transaction details.
              Returns "Not Found" message if transaction or user is not found.
    """
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    if not id:
        return jsonify(not_found), 404
    transaction = storage.get(Transaction, id)
    if not transaction and transaction._id in user.transactions:
        return jsonify(not_found), 404
    txn_data = request.get_json()
    if not txn_data:
        return jsonify(not_found), 404
    for key, value in txn_data.items():
        setattr(transaction, key, value)
    transaction.update()
    return jsonify(transaction.to_dict())

@app_views.route("/summery", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from('documentation/transaction/txn_summery.yml')
def txn_summary():
    """
    Endpoint to retrieve transaction summaries based on year and month for a user.

    Retrieves user identity, validates user existence, retrieves query parameters for year and month,
    performs database query to retrieve transaction summaries for the specified period.

    Returns:
        JSON: JSON response with transaction summaries based on year and month.
              Returns "Not Found" message if user is not found or if data retrieval fails.
    """
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    get_data = request.get_json()
    if not get_data:
        return jsonify(not_found), 404
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    result = storage.search(user, get_data.get("year"),
                            get_data.get("month"), page,
                            page_size)
    return jsonify(result)
