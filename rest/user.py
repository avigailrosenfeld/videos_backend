from email import message
import json
from flask import request, jsonify
from flask.wrappers import Response
from flask import current_app as app
from db.models import User
from flask_restful import Resource
from errors import InternalServerError, SchemaValidationError, UserNotFoundError, EmailAlreadyExistError
from rest.jwt import jwt_admin_required
from db.dal_mysql.dal_users import DalUsers
import bcrypt
from app import db


class UsersApi(Resource):
    decorators = [jwt_admin_required]

    def get(self):
        users = DalUsers.get_all_users()
        return Response(users, mimetype="application/json", status=200)

    def post(self):
        try:
            body = request.get_json()
            if not body:
                raise SchemaValidationError
            password = body.get('password')
            if not password:
                return jsonify(message="No Password"), 401
            body['password'] = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            user_id = DalUsers.create_user(User(**body))
            return Response(json.dumps({"id": user_id}), status=201, mimetype="application/json")
        except Exception as e:
            return Response(json.dumps({'message': 'Error UsersApi -> post() '}), mimetype="application/json", status=500)


class UserApi(Resource):
    decorators = [jwt_admin_required]

    def put(self, id):
        body = request.get_json()
        try:
            user_id = DalUsers.update_user(body, id)
        except Exception as e:
            return Response(json.dumps({"message": e}), status=400, mimetype="application/json")
        return Response(json.dumps({"id": user_id}), status=200, mimetype="application/json")

    def get(self, id):
        try:
            user = DalUsers.get_user_by_id(id)
            if not user:
                return Response(json.dumps({'message': 'User not found in database'}), mimetype="application/json", status=400)
            return Response(json.dumps(user.as_dict()), mimetype="application/json", status=200)
        except Exception as e:
            return Response(json.dumps({'message': 'Error UserApi -> get() '}), mimetype="application/json", status=500)

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return "", 200
