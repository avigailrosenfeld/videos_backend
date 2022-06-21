from flask import request, jsonify
from flask.wrappers import Response
from flask import current_app as app
from pyparsing import null_debug_action
from db.models import User
from flask_restful import Resource
from errors import InternalServerError, SchemaValidationError, UserNotFoundError, EmailAlreadyExistError
from rest.jwt import jwt_admin_required
import bcrypt


class VideosApi(Resource):
    decorators = [jwt_admin_required]

    def get(self):
        return

    def post(self):
        try:
            files = request.files
            a = 0
            # print("File uploaded")
            # print(file)

            # res = make_response(jsonify({"message": "File uploaded"}), 200)

            # return res
            # return {"id": str(id)}, 201
            return
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError
