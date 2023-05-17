import allure

from core.pages.auth import AuthPage
from core.pages.settings_org_tree import SettingsOrgTree


class TestLogoutFunctionality:

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
