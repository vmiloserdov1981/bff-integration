import requests


class BaseApiClient:
    def __init__(self, token: str = ''):
        self.auth = f'Bearer {token}'

    def append_auth(self, kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if 'Authorization' not in kwargs['headers']:
            kwargs['headers']['Authorization'] = self.auth

    def get(self, url, params=None, **kwargs) -> requests.Response:
        self.append_auth(kwargs)
        return requests.get(url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> requests.Response:
        self.append_auth(kwargs)
        return requests.post(url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs) -> requests.Response:
        self.append_auth(kwargs)
        return requests.put(url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs) -> requests.Response:
        self.append_auth(kwargs)
        return requests.patch(url, data=data, **kwargs)

    def delete(self, url, **kwargs) -> requests.Response:
        self.append_auth(kwargs)
        return requests.delete(url, **kwargs)
