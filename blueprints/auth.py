from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from errors import InternalServerError, SchemaValidationError, EmailAlreadyExistError
from flask_mongoengine import DoesNotExist
from db.models import User
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
        user = User(**body).save()
        return {}, 201
    except NotUniqueError:
        raise EmailAlreadyExistError
    except ValidationError:
        raise SchemaValidationError
    except Exception as e:
        raise InternalServerError


@auth.route('/login', methods=['POST'])
def login():
    if not request.json:
        return jsonify(message="No Data"), 401
    email = request.json.get("email")
    password = request.json.get("password")
    try:
        user = User.objects.get(email=email)
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify(message="Bad Email or Password"), 401
        access_token = create_access_token(identity=email)
        response = jsonify(message="login successful",
                           access_token=access_token)
        return response, 201
    except DoesNotExist:
        return jsonify(message="Bad Email or Password"), 401
    except Exception as e:
        return jsonify(message="WTF"), 401


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    response = jsonify({"msg": "logout successful"})
    return response, 200
