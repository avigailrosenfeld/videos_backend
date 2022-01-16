import os
from os.path import join, dirname
from decouple import Config, RepositoryEnv
import sys


class BaseConfig(object):
    env_config = os.environ
    if len(sys.argv) > 1:
        env_file = sys.argv[1]
        env_path = join(dirname(__file__), env_file)
        env_config = Config(RepositoryEnv(env_path)).repository.data

    SECRET_KEY = env_config["SECRET_KEY"]
    DEBUG = True
    MONGODB_DB = env_config["DB_NAME"]
    MONGODB_HOST = env_config["DB_HOST"]
    MONGODB_PORT = int(env_config["DB_PORT"])
    MONGODB_USERNAME = env_config["DB_USER"]
    MONGODB_PASSWORD = env_config["DB_PASS"]
