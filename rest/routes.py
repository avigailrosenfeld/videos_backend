from rest.user import UsersApi, UserApi
from rest.video import VideosApi


def initialize_routes(api):
    api.add_resource(UsersApi, "/users")
    api.add_resource(VideosApi, "/videos")
    api.add_resource(UserApi, "/users/<id>")
