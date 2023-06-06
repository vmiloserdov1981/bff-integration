import allure
from playwright.sync_api import expect

from core.consts.timeouts import Timeouts
from core.models.unit_type import UnitType
from core.models.user import User
from core.pages.rules import RulesPage


class TestRulesPage:

    @allure.id('371')
    @allure.title('Создание экспертного правила')
    def test_creating_rule_ui(self,
                              existing_equipment_type_and_brand,
                              unit_type_scaffold: UnitType,
                              default_user: User,
                              rules_page: RulesPage,
                              rules_name: str,
                              description: str,
                              description_edit: str,
                              unit_type_name: str,
                              unit_mark_name: str,
                              start_frequency='Каждую минуту'):

        with allure.step('Открыта страница "Экспертные правила"'):
            rules_page.check_specific_locators()

        with allure.step('Выбрать тип оборудования'):
            rules_page.select_from_dropdown(dropdown=rules_page.dropdown_choice_type_equipment,
                                            item=rules_page.choice_type_equipment(name=unit_type_name))

        with allure.step('Выбрать марку'):
            rules_page.select_from_dropdown(dropdown=rules_page.dropdown_choice_brand,
                                            item=rules_page.choice_brand(name=unit_mark_name))

        with allure.step('Нажать на кнопку - "Создать правило"'):
            rules_page.create_rules_locator.click()

        with allure.step('Ввести название для правила'):
            rules_page.rule_name_locator.type(rules_name)

        with allure.step('Выбрать частоту запуска правила: "Каждую минуту"'):
            rules_page.select_from_dropdown(dropdown=rules_page.start_frequency_dropdown,
                                            item=rules_page.choice_start_frequency(name=start_frequency))

        with allure.step('Ввести описание для правила'):
            rules_page.rule_description_locator.type(description)

        with allure.step('Нажать на кнопку "Сохранить"'):
            rules_page.save_rules_btn.click()

        with allure.step('Убедиться, что новое правило отображается на странице'):
            expect(rules_page.check_rule_display(name=rules_name)).to_have_count(1)

    @allure.id('379')
    @allure.title('Удаление экспертного правила')
    def test_deleting_rule_ui(self, existing_equipment_type_and_brand, unit_type_scaffold: UnitType, default_user: User,
                              rules_page: RulesPage, rules_name: str, description: str, description_edit: str,
                              unit_type_name: str, unit_mark_name: str):

        with allure.step('Открыта страница "Экспертные правила"'):
            rules_page.check_specific_locators()

        with allure.step('Выбрать тип оборудования'):
            rules_page.select_from_dropdown(dropdown=rules_page.dropdown_choice_type_equipment,
                                            item=rules_page.choice_type_equipment(name=unit_type_name))

        with allure.step('Выбрать марку'):
            rules_page.select_from_dropdown(dropdown=rules_page.dropdown_choice_brand,
                                            item=rules_page.choice_brand(name=unit_mark_name))

        with allure.step('Убедиться, что правило отображается на странице'):
            expect(rules_page.check_rule_display(name=rules_name)).to_have_count(1)

        with allure.step('Нажать на кнопку корзины - "Удалить правило"'):
            rules_page.delete_rule_btn.click()
            rules_page.wait(4000)
