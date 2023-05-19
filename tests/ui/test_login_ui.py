from http import HTTPStatus

import allure

from core.consts.timeouts import Timeouts
from core.models.user import User
from core.pages.auth import AuthPage
from core.pages.settings_org_tree import SettingsOrgTree


class TestLoginUi:

    @allure.id('266')
    @allure.title('Пользователь может войти в систему')
    def test_correct_login_ui(self, default_user: User, auth_page: AuthPage):
        with allure.step('Открыта страница логина'):
            auth_page.check_specific_locators()

        with allure.step('Ввести логин пользователя'):
            auth_page.login_input.type(text=default_user.login, delay=Timeouts.TYPE_DELAY, timeout=Timeouts.DEFAULT)

        with allure.step('Ввести пароль пользователя'):
            auth_page.password_input.type(text=default_user.password,
                                          delay=Timeouts.TYPE_DELAY,
                                          timeout=Timeouts.DEFAULT)

        with allure.step('Нажать на кнопку Войти'):
            with auth_page.expect_response(auth_page.session_response_lambda) as response_info:
                auth_page.submit_button.click(timeout=Timeouts.DEFAULT)
                response = response_info.value

        with allure.step('Session request returns 200'):
            assert (response.status == HTTPStatus.OK), f'Expecting status OK, got {response.status} instead'

    @allure.id('542')
    @allure.title('Пользователь может выйти из системы')
    def test_logout_functionality(self, orgs_page: SettingsOrgTree, front_url: str):
        with allure.step('Кнопка "Выход из аккаунта" доступна'):
            orgs_page.sidebar.check_specific_locators()

        with allure.step('Нажать на кнопку "Выход из аккаунта"'):
            orgs_page.sidebar.logout_button.click()

        with allure.step('Открыта страница логина'):
            auth_page = AuthPage(page=orgs_page.page, host=front_url)
            auth_page.check_specific_locators()

    @allure.id('267')
    @allure.title('Пользователь не может войти в систему с неверными данными')
    def test_wrong_login_ui(self, unknown_user: User, auth_page: AuthPage):
        with allure.step('Открыта страница логина'):
            auth_page.check_specific_locators()

        with allure.step('Ввести неизвестный логин пользователя'):
            auth_page.login_input.type(text=unknown_user.login, delay=Timeouts.TYPE_DELAY, timeout=Timeouts.DEFAULT)

        with allure.step('Ввести неизвестный пароль пользователя'):
            auth_page.password_input.type(text=unknown_user.password,
                                          delay=Timeouts.TYPE_DELAY,
                                          timeout=Timeouts.DEFAULT)

        with allure.step('Нажать на кнопку Войти'):
            with auth_page.expect_response(auth_page.session_credentials_lambda) as response_info:
                auth_page.submit_button.click(timeout=Timeouts.DEFAULT)
                response = response_info.value

        # TODO: когда появится валидация ошибок на фронте, добавить её сюда

        with allure.step('Session request returns 401'):
            assert (response.status == HTTPStatus.UNAUTHORIZED
                    ), f'Expecting status UNAUTHORIZED, got {response.status} instead'
