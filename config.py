import os
from dotenv import load_dotenv
from pathlib import Path
from os.path import join, dirname
import sys


class BaseConfig(object):
    env_file = sys.argv[1]
    dotenv_path = Path(join(dirname(__file__), env_file))
    a = load_dotenv(dotenv_path=dotenv_path)

    SECRET_KEY = os.environ["SECRET_KEY"]
    DEBUG = True
    MONGODB_DB = os.environ["DB_NAME"]
    MONGODB_HOST = os.environ["DB_HOST"]
    MONGODB_PORT = int(os.environ["DB_PORT"])
    MONGODB_USERNAME = os.environ["DB_USER"]
    MONGODB_PASSWORD = os.environ["DB_PASS"]
