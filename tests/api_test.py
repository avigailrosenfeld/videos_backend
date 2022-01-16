
from pymongo import MongoClient
from decouple import Config, RepositoryEnv
from unittest import TestCase
from os.path import join
from tests.users import UsersTests


API_URL: str = "http://localhost:8000"


class APITestCase(TestCase):
    def setUp(self):
        env_path = join('/workspaces/videos_backend', 'test.env')
        env_config = Config(RepositoryEnv(env_path)).repository.data

        if '127.0.0.1' not in env_config["DB_HOST"] or 'tests' not in env_config["DB_HOST"]:
            raise Exception("not local db")

        mongo_client = MongoClient(env_config["DB_HOST"])
        db = mongo_client.tests
        for collection in db.list_collection_names():
            db[collection].drop()

    def api_test(self) -> None:
        APITestCase.users()

    @staticmethod
    def users() -> None:
        users_test = UsersTests(API_URL)
        users_test.run_tests()
