

from api.v1.views import app_views
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from models import storage
from models.user import User
from models.utility import taken_value, encrypt, decrypt

@app_views.route("/register", methods=["POST"], strict_slashes=False)
def user_register():
    user_data = request.get_json()
    required_fields = [
        'first_name', 'last_name', 'email', 'username', 'password'
        ]
    for field in required_fields:
        md_field = field.replace('_', ' ').capitalize()
        if not user_data.get(field):
            return jsonify(f"{md_field} is required"), 400
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
        user = storage.filter(User, "email", login_data["email"])
        if user:
            if decrypt(login_data["password"], user.password):
                print(user)
                return jsonify({"token": create_access_token(identity=user.email)})
            else:
                return jsonify("Password is not correct"), 401
        else:
            return jsonify("Email is not found"), 404
    else:
        return jsonify("data not found"), 404