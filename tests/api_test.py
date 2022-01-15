
from unittest import TestCase
import requests


API_URL = "http://localhost:8000"


class APITestCase(TestCase):
    def create_user_test(self):
        user_data = {"name": "aa", "password": "1234", "email": "bb@a.a"}
        response = requests.post(f'{API_URL}/users', json=user_data)
        self.assertEqual(response.status_code, 201)
