from pydantic import BaseModel


class User(BaseModel):
    login: str = ''
    password: str = ''

    @property
    def body_for_authorize(self) -> dict:
        body = {
            'client_ident': self.login,
            'password': self.password
        }
        return body
