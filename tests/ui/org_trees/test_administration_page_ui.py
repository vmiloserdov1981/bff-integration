import allure
from playwright.sync_api import expect

from core.clients.bff_api import BffApiClient
from core.models.unit_type import UnitType
from core.models.user import User
from core.pages.settings_org_tree import SettingsOrgTree


class TestAdministrationPage:

    @allure.id('127')
    @allure.title('Проверка работы опций агрегата')
    def test_checking_implement_options_unit_ui(
            self, existing_equipment_type_and_brand, bff_client: BffApiClient, unit_type_scaffold: UnitType,
            default_user: User, orgs_page: SettingsOrgTree, company_name: str, branch_name: str, unit_name: str,
            unit_type_name: str, unit_mark_name: str, root_unit_node_name: str, create_company, existing_company,
            child_unit_node_name: str, unit_type_ids_to_delete: list, root_node_ids_to_delete: list):

        with allure.step('Открыта страница администрирования'):
            orgs_page.check_specific_locators()

        with allure.step('Нажать на локатор - Кампания '):
            orgs_page.node_menu_button_place_locator_by_name(name=company_name).click()

        with allure.step('Добавление сущности - "агрегат"'):
            orgs_page.lvl2_add_node_button.click()

        with allure.step('Выбрать тип элемента "агрегат"'):
            orgs_page.select_from_dropdown(dropdown=orgs_page.create_form.element_type_dropdown,
                                           item=orgs_page.create_form.unit_dropdown_option)

        with allure.step('Ввести наименование агрегата'):
            orgs_page.create_form.name_input.type(unit_name)

        with allure.step('Выбрать тип и марку агрегата'):
            orgs_page.select_from_dropdown(dropdown=orgs_page.create_form.unit_type_dropdown,
                                           item=orgs_page.create_form.dropdown_option_by_name(name=unit_type_name))

        with allure.step('Убедиться, что выбрана нужная марка агрегата'):
            expect(orgs_page.locator_entity_name(name=unit_mark_name)).to_have_count(1)

        with allure.step('Включить свитчер "Показывать в общем списке"'):
            orgs_page.turn_on_show_general_list_switch.click()
            orgs_page.edit_form.confirm_button.click()

        with allure.step('Раскрыть контекстное меню агрегата'):
            orgs_page.node_menu_button_locator.click()

        with allure.step('Опции агрегата содержит пункт "Скрыть из общего списка"'):
            orgs_page.check_options_hide_from_the_list()

        with allure.step('Опции агрегата содержит пункт "Редактировать"'):
            orgs_page.check_edit_unit()

        with allure.step('Опции агрегата содержит пункт "Удалить"'):
            orgs_page.check_del_unit()

        with allure.step('Перейти на страницу "Мониторинг"'):
            orgs_page.sidebar.org_tree_button.click()

        with allure.step('На странице мониторинга агрегат отображается в общем списке'):
            orgs_page.disclose_company_dropdown(name=company_name).click()
            expect(orgs_page.unit_in_general_list(name=unit_name)).to_have_count(1)

        with allure.step('Перейти на страницу "Администрирования"'):
            orgs_page.sidebar.settings_button.click()

        with allure.step('Нажать на локатор - Кампания '):
            orgs_page.node_locator_by_name(name=company_name).click()

        with allure.step('Раскрыть контекстное меню агрегата'):
            orgs_page.unit_menu_button_locator(name=unit_name).click()

        with allure.step('Нажать на опцию агрегата "Скрыть из общего списка"'):
            orgs_page.options_hide_from_the_list.click()

        with allure.step('Перейти на страницу "Мониторинг"'):
            orgs_page.sidebar.org_tree_button.click()
            orgs_page.check_monitoring_page()

        with allure.step('На странице мониторинга агрегат НЕ отображается в общем списке'):
            expect(orgs_page.disclose_company_dropdown(name=company_name)).to_have_count(0)
            expect(orgs_page.unit_in_general_list(name=unit_name)).to_have_count(0)

        with allure.step('Перейти на страницу "Администрирования"'):
            orgs_page.sidebar.settings_button.click()

        with allure.step('Нажать на локатор - Кампания '):
            orgs_page.node_locator_by_name(name=company_name).click()

        with allure.step('Раскрыть контекстное меню агрегата'):
            orgs_page.unit_menu_button_locator(name=unit_name).click()

        with allure.step('Опции агрегата содержит пункт "Показать в общем списке"'):
            orgs_page.check_options_show_from_the_list()

        with allure.step('Нажать на опцию агрегата "Редактировать"'):
            orgs_page.edit_node_menu_option.click()

        with allure.step('Переключатель "Показывать в общем списке" неактивен.'):
            orgs_page.check_switcher_show_in_list_not_active()

        with allure.step('Нажать на кнопку "сохранить"'):
            orgs_page.edit_form.confirm_button.click()

        with allure.step('Раскрыть контекстное меню агрегата'):
            orgs_page.unit_menu_button_locator(name=unit_name).click()

        with allure.step('Нажать на опцию агрегата "Показать в общем списке"'):
            orgs_page.options_show_from_the_list.click()

        with allure.step('Перейти на страницу "Мониторинг"'):
            orgs_page.sidebar.org_tree_button.click()
            orgs_page.check_monitoring_page()

        with allure.step('На странице мониторинга агрегат отображается в общем списке'):
            expect(orgs_page.disclose_company_dropdown(name=company_name)).to_have_count(1)
            orgs_page.disclose_company_dropdown(name=company_name).click()
            expect(orgs_page.unit_in_general_list(name=unit_name)).to_have_count(1)

        with allure.step('Перейти на страницу "Администрирования"'):
            orgs_page.sidebar.settings_button.click()

        with allure.step('Нажать на локатор - Кампания '):
            orgs_page.node_locator_by_name(name=company_name).click()

        with allure.step('Раскрыть контекстное меню агрегата'):
            orgs_page.unit_menu_button_locator(name=unit_name).click()

        with allure.step('Выбрать из меню опцию удаления'):
            orgs_page.delete_node_menu_option.click()

        with allure.step('Открыто модальное окно подтверждения удаления'):
            expect(orgs_page.delete_form.wrapper).to_have_count(1)
            orgs_page.delete_form.check_specific_locators()

        with allure.step('Нажать на кнопку подтверждения удаления'):
            orgs_page.delete_form.confirm_button.click()

        with allure.step('Убедиться, что сущность агрегат - удалена'):
            expect(orgs_page.node_locator_by_name(name=unit_name)).to_have_count(0)
