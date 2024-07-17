
from api.v1.views import app_views
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import storage
from models.user import User
from models.transaction import Transaction
from models.utility import not_found

@app_views.route("/transactions", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_transaction():

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
    cache.delete_memoized(get_all_transaction, user_id)
    return jsonify(transaction.to_dict() )


@app_views.route("/transactions", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_all_transaction():

    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    all_txn = [value
               for _, value in storage.all(Transaction).items()
               if value["_id"] in user.transactions]
    return jsonify(all_txn)


@app_views.route("/transactions/<id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_transaction(id=None):

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
def update_transaction(id=None):

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
def txn_summery():
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