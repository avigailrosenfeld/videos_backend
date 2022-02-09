from flask import request, request
from flask.wrappers import Response
from flask import current_app as app
from db.models import Video
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from errors import InternalServerError, SchemaValidationError, VideoNotFoundError, EmailAlreadyExistError
from rest.jwt import jwt_admin_required
from config import FileConfig
import os


class VideosApi(Resource):
    decorators = [jwt_admin_required]

    def get(self):
        videos = Video.objects().to_json()
        return Response(videos, mimetype="application/json", status=200)

    def post(self):
        try:
            body = request.files['videofile']
            if not body:
                raise SchemaValidationError
            uploads_dir = os.path.join(FileConfig.PATH_VIDEOS)
            # os.makedirs(uploads_dir, exists_ok=True)
            body.save(os.path.join(uploads_dir, body.filename))
            # save each "charts" file
            for file in request.files.getlist('charts'):
                file.save(os.path.join(
                    uploads_dir, file.name))
            return {"id": str(123)}, 201
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
