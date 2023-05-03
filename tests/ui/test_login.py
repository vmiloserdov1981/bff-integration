import allure

from http import HTTPStatus

from core.consts.timeouts import Timeouts
from core.models.user import User
from core.pages.auth import AuthPage


class TestLogin:

    @allure.id('266')
    @allure.title('Пользователь может войти в систему')
    def test_correct_login(self, default_user: User, auth_page: AuthPage):
        with allure.step('Открыта страницу логина'):
            auth_page.check_specific_locators()

        with allure.step('Ввести логин пользователя'):
            auth_page.login_input.type(text=default_user.login, delay=Timeouts.TYPE_DELAY, timeout=Timeouts.DEFAULT)

        with allure.step('Ввести пароль пользователя'):
            auth_page.password_input.type(text=default_user.login, delay=Timeouts.TYPE_DELAY, timeout=Timeouts.DEFAULT)

        with allure.step('Нажать на кнопку Войти'):
            with auth_page.expect_response(auth_page.session_response_lambda) as response_info:
                auth_page.submit_button.click(timeout=Timeouts.DEFAULT)
                response = response_info.value

        with allure.step('Session request returns 200'):
            assert response.status == HTTPStatus.OK, f'Expecting status OK, got response.status instead'




