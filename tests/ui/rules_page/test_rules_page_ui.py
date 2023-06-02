import allure
from playwright.sync_api import expect

from core.consts.timeouts import Timeouts
from core.models.user import User
from core.pages.rules import RulesPage


class TestRulesPage:

    @allure.id('398')
    @allure.title('Создание, редактирование и удаление экспертного правила')
    def test_creating_rule_ui(self, existing_equipment_type_and_brand, default_user: User, rules_page: RulesPage,
                              rules_name: str, description: str, description_edit: str):

        with allure.step('Открыта страница администрирования'):
            rules_page.check_specific_locators()

        with allure.step('Выбрать тип оборудования'):
            rules_page.select_from_dropdown(dropdown=rules_page.dropdown_choice_type_equipment,
                                            item=rules_page.choice_type_equipment)

        with allure.step('Выбрать марку'):
            rules_page.select_from_dropdown(dropdown=rules_page.dropdown_choice_brand, item=rules_page.choice_brand)

        with allure.step('Создание сущности - экспертное правило'):
            rules_page.create_rules_locator.click()
            rules_page.rule_name_locator.type(rules_name)
            rules_page.rule_description_locator.type(description)
            rules_page.wait(4000)
