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
        users = User.query.get().all()

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
            new_user = User(**body)
            db.session.add(new_user)
            db.session.commit()
            return {"id": str(new_user.id)}, 201
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
        user = User.query.get(id=id).first()
        user = User(**body)
        db.session.commit()
        return "", 200

    def get(self, id):
        try:
            user = DalUsers.get_user_by_id(id)
            if not user:
                return Response(json.dumps({'message': 'User not found in database'}), mimetype="application/json", status=400)
            return Response(json.dumps(user.as_dict()), mimetype="application/json", status=200)
        except Exception as e:
            if False:
                return jsonify(message="DoesNotExist"), 401
            if False:
                return jsonify(message="ValidationError"), 401
            return jsonify(message="Unknown"), 500

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return "", 200
