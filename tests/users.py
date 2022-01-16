import requests


class UsersTests():
    def __init__(self, api_url: str) -> None:
        self._api_url = api_url
        self._access_token = None
        self._user_id = None

    def run_tests(self) -> None:
        self._create_user()
        self._get_existing_user()
        self._get_not_existing_user()
        self._login()

    def _create_user(self) -> None:
        user_data = {"name": "achia", "password": "1234",
                     "email": "achia@test.com"}
        response = requests.post(f'{self._api_url}/users', json=user_data)
        assert response.status_code == 201, 'cant create user'
        self._user_id = response.json().get('id')

    def _get_existing_user(self) -> None:
        response = requests.get(f'{self._api_url}/users/{self._user_id}')
        assert response.status_code == 200, 'cant get existing user'
        assert response.json().get('name') == 'achia', 'get user wrong name'
        assert response.json().get('email') == 'achia@test.com', 'get user wrong email'
        assert response.json().get('password') != '1234', 'get user password not encrypted'

    def _get_not_existing_user(self) -> None:
        response = requests.get(
            f'{self._api_url}/users/61e4107dab0894a2861fed80')
        assert response.status_code == 400, 'get not existing user return not 400'
        assert response.json().get(
            'message') == 'User not found in database', 'get not existing user wrong message'
        response = requests.get(f'{self._api_url}/users/123456')
        assert response.status_code == 400, 'get invalid id not return 400'

    def _login(self) -> None:
        user_data = {"password": "1234", "email": "achia@test.com"}
        response = requests.post(f'{self._api_url}/login', json=user_data)
        assert response.status_code == 201, 'login failed'
        assert response.json().get(
            'message') == 'Login Succeeded!', 'login success wrong message'
        self._access_token = response.json().get('access_token')
        assert self._access_token is not None, 'login access token is None'
