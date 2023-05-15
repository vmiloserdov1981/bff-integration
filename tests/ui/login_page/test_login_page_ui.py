import allure

from core.consts.timeouts import Timeouts
from core.models.user import User
from core.pages.auth import AuthPage


class TestLoginPage:

    @allure.id('265')
    @allure.title('Проверка элементов и текста страницы логина')
    def test_login_page_ui(self, default_user: User, auth_page: AuthPage):
        with allure.step('Открыта страница логина'):
            auth_page.check_specific_locators()

        with allure.step('Заголовок страницы логина корректный'):
            auth_page.check_form_title_text()

        with allure.step('Подзаголовок страницы логина корректный'):
            auth_page.check_form_subtitle_text()

        with allure.step('Название поля "Логин" корректное'):
            auth_page.check_login_input_title()

        with allure.step('Название поля "Пароль" корректное'):
            auth_page.check_password_input_title()

        with allure.step('Название кнопки "Войти" корректное'):
            auth_page.check_submit_button_text()

        with allure.step('Кнопка "Войти" не активна'):
            auth_page.check_disabled_submit_button()

        with allure.step('Ввести логин пользователя'):
            auth_page.login_input.type(text=default_user.login, delay=Timeouts.TYPE_DELAY, timeout=Timeouts.DEFAULT)

        with allure.step('Введенный логин отображается'):
            auth_page.check_login_input_value(login=default_user.login)

        with allure.step('Кнопка "Войти" не активна'):
            auth_page.check_disabled_submit_button()

        with allure.step('Ввести пароль пользователя'):
            auth_page.password_input.type(text=default_user.password,
                                          delay=Timeouts.TYPE_DELAY,
                                          timeout=Timeouts.DEFAULT)

        with allure.step('Введенный пароль не отображается'):
            auth_page.check_password_input_value_hidden(password=default_user.password)

        with allure.step('Кнопка отображения пароля активна и показывает пароль'):
            auth_page.password_display_button.click()
            auth_page.check_password_input_value_visible(password=default_user.password)

        with allure.step('Кнопка "Войти" активна'):
            auth_page.check_enabled_submit_button()
