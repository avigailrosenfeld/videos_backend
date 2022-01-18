from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, \
    set_access_cookies, unset_jwt_cookies, get_jwt
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from errors import InternalServerError, SchemaValidationError, EmailAlreadyExistError
from flask_mongoengine import DoesNotExist
from flask import current_app as app
from db.models import User
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
        app.logger.error(e)
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
        response = jsonify(message="login successful")
        set_access_cookies(response, access_token)
        return response, 201
    except DoesNotExist:
        return jsonify(message="Bad Email or Password"), 401
    except Exception:
        return jsonify(message="WTF"), 401


@auth.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200


# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original respone
#         return response
