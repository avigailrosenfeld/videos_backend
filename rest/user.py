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


class UsersApi(Resource):
    decorators = [jwt_admin_required]

    def get(self):
        try:
            users = DalUsers.get_all_users()
            response = []
            for user in users:
                response.append(user.as_dict())
            return Response(json.dumps(response), mimetype="application/json", status=200)
        except Exception as e:
            return Response(json.dumps({'message': 'Internal Server Error'}), mimetype="application/json", status=500)

    def post(self):
        try:
            body = request.get_json()
            if not body:
                raise SchemaValidationError
            password = body.get('password')
            if not password:
                return Response(json.dumps({'message': 'No Password'}), mimetype="application/json", status=401)
            body['password'] = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            user_id = DalUsers.create_user(User(**body))
            return Response(json.dumps({"id": user_id}), status=201, mimetype="application/json")
        except Exception as e:
            return Response(json.dumps({'message': 'Internal Server Error'}), mimetype="application/json", status=500)


class UserApi(Resource):
    decorators = [jwt_admin_required]

    def put(self, id):
        body = request.get_json()
        try:
            user_id = DalUsers.update_user(body, id)  # type: ignore
            return Response(json.dumps({"id": user_id}), status=200, mimetype="application/json")
        except Exception as e:
            return Response(json.dumps({"message": e}), status=400, mimetype="application/json")

    def get(self, id):
        try:
            user = DalUsers.get_user_by_id(id)
            if not user:
                return Response(json.dumps({'message': 'Not Exist'}), mimetype="application/json", status=404)
            return Response(json.dumps(user.as_dict()), mimetype="application/json", status=200)
        except Exception as e:
            return Response(json.dumps({'message': 'Internal Server Error'}), mimetype="application/json", status=500)

    def delete(self, id):
        try:
            DalUsers.delete_user_by_id(id)
            return Response(json.dumps({}), mimetype="application/json", status=200)
        except Exception as e:
            return Response(json.dumps({'message': 'Not Exist'}), mimetype="application/json", status=404)
