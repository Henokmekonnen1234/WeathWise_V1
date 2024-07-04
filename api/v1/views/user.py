

from api.v1.views import app_views
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import storage
from models.user import User
from models.utility import taken_value, encrypt, decrypt, not_found
from models.utility import is_user_valid

@app_views.route("/register", methods=["POST"], strict_slashes=False)
def user_register():
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
def login():
    login_data = request.get_json()
    if login_data:
        user = storage.filter(User, "username", login_data["username"])
        if user:
            print(user)
            if decrypt(login_data["password"], user.password):
                token = create_access_token(identity=str(user._id))
                return jsonify({"token": token})
            else:
                return jsonify("Password is not correct"), 401
        else:
            return jsonify("Username is not found"), 404
    else:
        return jsonify("data not found"), 404


@app_views.route("/user", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_user():

    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify(not_found), 404
    user._id = str(user._id)
    return jsonify(user.to_dict())


@app_views.route("/user", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_user():

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