from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from db.dal_mysql.dal_users import DalUsers
from db.models import User
from errors import InternalServerError, SchemaValidationError, EmailAlreadyExistError, UserNotFoundError
from constants import ACCESS_EXPIRES
from app import jwt_redis_blocklist
import bcrypt
from flask.wrappers import Response
import json


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    try:
        body = request.get_json()
        if not body:
            raise SchemaValidationError
        password = body.get('password')
        if not password:
            return Response(json.dumps({'message': 'No Password'}), mimetype="application/json", status=401)
        body['password'] = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        DalUsers.create_user(User(**body))
        return Response(json.dumps({'message': 'Success'}), mimetype="application/json", status=201)
    except Exception as e:
        return Response(json.dumps({'message': 'Register Failed'}), mimetype="application/json", status=500)


@auth.route('/login', methods=['POST'])
def login():
    if not request.json:
        raise SchemaValidationError
    email = request.json.get("email")
    password = request.json.get("password")
    try:
        user = DalUsers.get_user_by_email(email=email)
        if not user:
            raise UserNotFoundError
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return Response(json.dumps({'message': 'Bad Email or Password'}), mimetype="application/json", status=401)
        access_token = create_access_token(identity=email)
        return Response(json.dumps({'message': 'Login Successful'}, access_token=access_token), mimetype="application/json", status=201)
    except Exception as e:
        return Response(json.dumps({'message': 'Login failed'}), mimetype="application/json", status=500)


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return Response(json.dumps({'message': 'Logout Successful'}), mimetype="application/json", status=200)
    except Exception as e:
        return Response(json.dumps({'message': 'Logout failed'}), mimetype="application/json", status=500)
