from flask import Flask, jsonify, request
from config import BaseConfig
from db import initialize_db
from rest import initialize_api
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mongoengine import DoesNotExist
from blueprints.auth import auth

app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)

# JWT Config
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"  # change it


def init():
    app.config.from_object(BaseConfig)
    initialize_db(app)
    initialize_api(app)


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=8000, debug=True)
