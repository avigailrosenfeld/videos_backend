from flask import request, jsonify
from flask.wrappers import Response
from flask import current_app as app
from db.models import User
from flask_restful import Resource
from errors import InternalServerError, SchemaValidationError, UserNotFoundError, EmailAlreadyExistError
from rest.jwt import jwt_admin_required
import bcrypt
from app import db


class UsersApi(Resource):
    decorators = [jwt_admin_required]

    def get(self):
        users = User.query().all().to_json()
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
            userid = db.session.add(User(**body))
            db.session.commit()
            return {"id": str(userid)}, 201
        except Exception as e:
            if False:
                return jsonify(message="EmailAlreadyExistError"), 401
            if False:
                return jsonify(message="SchemaValidationError"), 401
            app.logger.error(e)
            raise InternalServerError


class UserApi(Resource):
    decorators = [jwt_admin_required]

    def put(self, id):
        body = request.get_json()
        user = User.query.get(id=id)
        user = User(**body)
        db.session.commit()
        return "", 200

    def get(self, id):
        try:
            users = User.query.get(id=id)
            users = users.to_json()
            return Response(users, mimetype="application/json", status=200)
        except Exception as e:
            if False:
                return jsonify(message="DoesNotExist"), 401
            if False:
                return jsonify(message="ValidationError"), 401

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return "", 200
