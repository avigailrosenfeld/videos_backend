from flask import request, jsonify
from flask.wrappers import Response
from flask import current_app as app
from pyparsing import null_debug_action
from db.models import Video
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from errors import InternalServerError, SchemaValidationError, VideoNotFoundError, EmailAlreadyExistError
from rest.jwt import jwt_admin_required
import bcrypt


class VideosApi(Resource):
    decorators = [jwt_admin_required]

    def get(self):
        videos = Video.objects().to_json()
        return Response(videos, mimetype="application/json", status=200)

    def post(self):
        try:
            body = request.get_json()
            if not body:
                raise SchemaValidationError
            # password = body.get('password')
            # if not password:
            #     return jsonify(message="No Password"), 401
            # body['password'] = bcrypt.hashpw(
            #     password.encode('utf-8'), bcrypt.gensalt())
            video = Video(**body).save()
            id = video.id
            return {"id": str(id)}, 201
        except NotUniqueError:
            raise EmailAlreadyExistError
        except ValidationError:
            raise SchemaValidationError
        except Exception as e:
            app.logger.error(e)
            raise InternalServerError


class VideoApi(Resource):
    decorators = [jwt_admin_required]

    def put(self, id):
        body = request.get_json()
        Video.objects.get(id=id).update(**body)
        return "", 200

    def get(self, id):
        try:
            videos = Video.objects.get(id=id)
            videos = videos.to_json()
            return Response(videos, mimetype="application/json", status=200)
        except DoesNotExist:
            raise VideoNotFoundError
        except ValidationError:
            raise SchemaValidationError

    def delete(self, id):
        video = Video.objects.get(id=id).delete()
        return "", 200
