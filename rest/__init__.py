from flask_restful import Api
from .routes import initialize_routes
from errors import errors
from blueprints.auth import auth

api = None


def initialize_api(app):
    app.logger.info("Initializing REST Apis")
    app.register_blueprint(auth)
    api = Api(app, errors=errors)
    initialize_routes(api)
