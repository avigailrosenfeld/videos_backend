
from pymongo import MongoClient
from decouple import Config, RepositoryEnv
from unittest import TestCase
from os.path import join
import requests


API_URL = "http://localhost:8000"


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

        self._access_token = None

    def api_test(self):
        self.create_user()
        self.login()

    def create_user(self):
        user_data = {"name": "aa", "password": "1234", "email": "bb@a.a"}
        response = requests.post(f'{API_URL}/users', json=user_data)
        self.assertEqual(response.status_code, 201)

    def login(self):
        user_data = {"password": "1234", "email": "bb@a.a"}
        response = requests.post(f'{API_URL}/login', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), 'Login Succeeded!')
        self._access_token = response.json().get('access_token')
        self.assertIsNotNone(self._access_token)
