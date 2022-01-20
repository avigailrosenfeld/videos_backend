from flask import Flask
from config import BaseConfig, RedisConfig
from flask_cors import CORS
from constants import ACCESS_EXPIRES
from flask_jwt_extended import JWTManager
import redis

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config.from_object(BaseConfig)
CORS(app)
jwt = JWTManager(app)

redis_config = RedisConfig()

jwt_redis_blocklist = redis.StrictRedis(
    host=redis_config.REDIS_HOST, port=redis_config.REDIS_PORT, db=0, decode_responses=True
)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


def init():
    from rest import initialize_api
    from db import initialize_db
    initialize_db(app)
    initialize_api(app)


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=8000, debug=True)
