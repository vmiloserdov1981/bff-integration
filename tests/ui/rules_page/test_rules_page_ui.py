import allure
from playwright.sync_api import expect

from core.consts.timeouts import Timeouts
from core.models.user import User
from core.pages.rules import RulesPage


class TestRulesPage:

    @allure.id('398')
    @allure.title('Создание, редактирование и удаление экспертного правила')
    def test_administration_page_ui(self, default_user: User, rules_page: RulesPage, rules_name: str, description: str,
                                    description_edit: str):

        with allure.step('Открыта страница администрирования'):
            rules_page.check_specific_locators()

        with allure.step('Выбрать тип оборудования'):
            rules_page.choose_type_equipment.click()

        with allure.step('Выбрать марку'):
            rules_page.choose_brand.click()

        with allure.step('Создание сущности - экспертное правило'):
            rules_page.create_rules_locator.click()
