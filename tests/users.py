from wsgiref import headers
import requests


class UsersTests():
    def __init__(self, api_url: str) -> None:
        self._api_url = api_url
        self._access_token = None
        self._user_id = None

    def run_tests(self) -> None:
        self._register()
        self._login()
        self._create_user()
        self._get_existing_user()
        self._get_not_existing_user()
        self._logout()
        self._create_user_after_logout()

    def _register(self) -> None:
        user_data = {"name": "achia", "password": "1234",
                     "email": "achia@test.com"}
        response = requests.post(f'{self._api_url}/register', json=user_data)
        assert response.status_code == 201, 'cant register'

    def _create_user(self) -> None:
        user_data = {"name": "avigail", "password": "1234",
                     "email": "avigail@test.com"}
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.post(f'{self._api_url}/users', json=user_data)
        assert response.status_code == 401, 'create user without token'
        response = requests.post(
            f'{self._api_url}/users', json=user_data, headers=headers)
        assert response.status_code == 201, 'cant create user'
        self._user_id = response.json().get('id')

    def _get_existing_user(self) -> None:
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.get(f'{self._api_url}/users/{self._user_id}')
        assert response.status_code == 401, 'get user without token'
        response = requests.get(
            f'{self._api_url}/users/{self._user_id}', headers=headers)
        assert response.status_code == 200, 'cant get existing user'
        assert response.json().get('name') == 'avigail', 'get user wrong name'
        assert response.json().get('email') == 'avigail@test.com', 'get user wrong email'
        assert response.json().get('password') != '1234', 'get user password not encrypted'

    def _get_not_existing_user(self) -> None:
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.get(
            f'{self._api_url}/users/61e4107dab0894a2861fed80', headers=headers)
        assert response.status_code == 400, 'get not existing user return not 400'
        assert response.json().get(
            'message') == 'User not found in database', 'get not existing user wrong message'
        response = requests.get(
            f'{self._api_url}/users/123456', headers=headers)
        assert response.status_code == 400, 'get invalid id not return 400'

    def _login(self) -> None:
        user_data = {"password": "1234", "email": "achia@test.com"}
        response = requests.post(f'{self._api_url}/login', json=user_data)
        assert response.status_code == 201, 'login failed'
        assert response.json().get(
            'message') == 'login successful', 'login success wrong message'
        self._access_token = response.json().get('access_token')
        assert self._access_token is not None, 'login access token is None'

    def _logout(self) -> None:
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.post(f'{self._api_url}/logout')
        assert response.status_code == 401, 'cant logout without token'
        response = requests.post(f'{self._api_url}/logout', headers=headers)
        assert response.status_code == 200, 'cant logout without token'

    def _create_user_after_logout(self) -> None:
        user_data = {"name": "chaim", "password": "1234",
                     "email": "chaim@test.com"}
        headers = {"Authorization": "Bearer " + self._access_token}
        response = requests.post(
            f'{self._api_url}/users', json=user_data, headers=headers)
        assert response.status_code == 401, 'create user after logout'
        assert response.json().get('msg') == 'Token has been revoked', 'token should be revoked'
