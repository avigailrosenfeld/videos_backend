from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from db.dal_mysql.dal_users import DalUsers
from db.models import User
from errors import InternalServerError, SchemaValidationError, EmailAlreadyExistError
from constants import ACCESS_EXPIRES
from app import jwt_redis_blocklist
import bcrypt


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    try:
        body = request.get_json()
        if not body:
            raise SchemaValidationError
        password = body.get('password')
        if not password:
            return jsonify(message="No Password"), 401
        body['password'] = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        DalUsers.create_user(User(**body))
        return {}, 201
    except Exception as e:
        # TODO
        if False:
            raise EmailAlreadyExistError
        if False:
            raise SchemaValidationError
        raise InternalServerError


@auth.route('/login', methods=['POST'])
def login():
    if not request.json:
        return jsonify(message="No Data"), 401
    email = request.json.get("email")
    password = request.json.get("password")
    try:
        user = DalUsers.get_user_by_email(email=email)
        if not user:
            return jsonify(message="User not exist"), 401
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify(message="Bad Email or Password"), 401
        access_token = create_access_token(identity=email)
        response = jsonify(message="login successful",
                           access_token=access_token)
        return response, 201
    except Exception as e:
        # TODO
        if False:
            return jsonify(message="Bad Email or Password"), 401
        return jsonify(message="WTF"), 401


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    response = jsonify({"msg": "logout successful"})
    return response, 200
