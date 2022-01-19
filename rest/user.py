from flask import request, jsonify
from flask.wrappers import Response
from flask import current_app as app
from db.models import User
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from errors import InternalServerError, SchemaValidationError, UserNotFoundError, EmailAlreadyExistError
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import bcrypt


def is_admin(func):
    def inner1(*args, **kwargs):
        verify_jwt_in_request()
        user = User.objects.get(email=get_jwt_identity())
        if not user.is_admin:
            return {'msg': 'only for admins'}, 401
        returned_value = func(*args, **kwargs)
        return returned_value
    return inner1


class UsersApi(Resource):
    decorators = [is_admin]

    def get(self):
        users = User.objects().to_json()
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
            user = User(**body).save()
            id = user.id
            return {"id": str(id)}, 201
        except NotUniqueError:
            raise EmailAlreadyExistError
        except ValidationError:
            raise SchemaValidationError
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError


class UserApi(Resource):
    decorators = [is_admin]

    def put(self, id):
        body = request.get_json()
        User.objects.get(id=id).update(**body)
        return "", 200

    def get(self, id):
        try:
            users = User.objects.get(id=id)
            users = users.to_json()
            return Response(users, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotFoundError
        except ValidationError:
            raise SchemaValidationError

    def delete(self, id):
        user = User.objects.get(id=id).delete()
        return "", 200
