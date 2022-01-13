from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mongoengine import DoesNotExist
from db.models import User
import bcrypt

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.json["email"]
    password = request.json["password"]
    try:
        user = User.objects.get(email=email)
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify(message="Bad Email or Password"), 401
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    except DoesNotExist:
        return jsonify(message="Bad Email or Password"), 401
    return jsonify(message="WTF"), 401
