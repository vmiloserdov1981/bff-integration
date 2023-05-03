import requests


class AuthApiClient:
    def __init__(self, host: str):
        self.host = host

    def authorize(self, body: dict) -> requests.Response:
        response = requests.post(url=f'{self.host}/api/v1/authorize', json=body)
        return response
