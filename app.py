from flask import Flask
from config import BaseConfig
from db import initialize_db
from rest import initialize_api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)
CORS(app)


def init():
    app.config.from_object(BaseConfig)
    initialize_db(app)
    initialize_api(app)


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=8000, debug=True)
