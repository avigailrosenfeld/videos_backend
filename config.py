import os
from os.path import join, dirname
from decouple import Config, RepositoryEnv
import sys
from typing import Dict, Any


def get_env_object():
    env_config = os.environ
    if len(sys.argv) > 1:
        env_file = sys.argv[1]
        env_path = join(dirname(__file__), env_file)
        env_config = Config(RepositoryEnv(env_path)).repository.data
    return env_config


env_config = get_env_object()


class BaseConfig(object):
    SECRET_KEY = env_config["SECRET_KEY"]
    DEBUG = True
    MONGODB_DB = env_config["DB_NAME"]
    MONGODB_HOST = env_config["DB_HOST"]
    MONGODB_PORT = int(env_config["DB_PORT"])
    MONGODB_USERNAME = env_config["DB_USER"]
    MONGODB_PASSWORD = env_config["DB_PASS"]


class FileConfig(object):
    PATH_VIDEOS = env_config["PATH_VIDEOS"]


class RedisConfig(object):
    REDIS_HOST = env_config["REDIS_HOST"]
    REDIS_PORT = int(env_config["REDIS_PORT"])
