from decouple import Config, RepositoryEnv
from unittest import TestCase
from os.path import join, dirname
from users import UsersTests


API_URL: str = "http://localhost:8000"


class APITestCase(TestCase):
    def setUp(self):
        APITestCase._prepare_db()
        self._users_tests = UsersTests(API_URL)

    @staticmethod
    def _prepare_db() -> None:
        env_path = join(dirname(__file__) + '/..', 'test.env')
        env_config = Config(RepositoryEnv(env_path)).repository.data

        if 'test' not in env_config["DB_NAME"]:
            raise Exception("not local db")
        # if 'test' in app.config.get('SQLALCHEMY_DATABASE_URI'):
        #   with app.app_context():
        #      db.engine.execute("DROP TABLE users;")
        # mmongo_client = MongoClient(env_config["DB_HOST"])
        # db = mongo_client.tests
        # for collection in db.list_collection_names():
        #     db[collection].drop()

    def runTest(self) -> None:
        self._users_tests.run_tests()
