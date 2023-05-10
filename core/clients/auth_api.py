import requests


class AuthApiClient:
    def __init__(self, host: str):
        self.host = host
        self.authorize_path = '/api/v1/authorize'

    def authorize(self, body: dict) -> requests.Response:
        response = requests.post(url=f'{self.host}{self.authorize_path}', json=body)
        return response
