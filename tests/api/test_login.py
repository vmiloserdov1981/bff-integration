import allure

from http import HTTPStatus

from core.clients.auth_api import AuthApiClient
from core.helpers.utils import check_response_status
from core.models.user import User


class TestLogin:

    @allure.id('')
    @allure.title('Пользователь может войти в систему')
    def test_correct_login(self, default_user: User, auth_client: AuthApiClient):
        with allure.step('Отправить запрос авторизации в API авторизации'):
            auth_response = auth_client.authorize(body=default_user.body_for_authorize)

        with allure.step('Код ответа - OK(200)'):
            check_response_status(given=auth_response.status_code, expected=HTTPStatus.OK)

        with allure.step('Тело ответа содержит токен авторизации'):
            response_json = auth_response.json()
            # TODO: Use model
            assert 'access_token' in response_json, 'Response should contain "access_token" key'

        with allure.step('Token is not empty'):
            # TODO: Use model
            assert response_json.get('access_token'), 'Access token should not be empty'

