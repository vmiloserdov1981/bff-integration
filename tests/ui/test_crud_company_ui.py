import allure
from http import HTTPStatus
from core.pages.settings_org_tree import SettingsOrgTree
from core.consts.timeouts import Timeouts
from core.models.org_nodes import CommonNode, RootNodeResponse, RootElem
from core.helpers.utils import check_response_status
from core.clients.bff_api import BffApiClient
from playwright.sync_api import expect


class TestCRUDCompany:
    @allure.id('129')
    @allure.title('Создание компании')
    def test_create_company(
            self,
            orgs_page: SettingsOrgTree,
            company_name: str,
            root_node_ids_to_delete: list,
            bff_client: BffApiClient,
    ):
        with allure.step('Проверка наличия локаторов'):
            orgs_page.check_specific_locators()

        with allure.step('Нажать на кнопку добавления компании'):
            orgs_page.add_tree_button.click()

        with allure.step('Открыто модальное окно добавления компании'):
            orgs_page.check_locator_visibility(orgs_page.create_form.wrapper)

        with allure.step('Ввести название компании'):
            orgs_page.create_form.name_input.type(
                text=company_name,
                delay=Timeouts.TYPE_DELAY,
                timeout=Timeouts.DEFAULT
            )

        with allure.step('Кнопка сохранения компании доступна'):
            orgs_page.check_locator_visibility(orgs_page.create_form.confirm_button)

        with allure.step('Нажать на кнопку "Добавить"'):
            root_node: CommonNode
            with orgs_page.expect_response(orgs_page.create_node_request_lambda(bff_client=bff_client)) as resp_info:
                orgs_page.create_form.confirm_button.click()
                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.CREATED)
                root_node = RootNodeResponse(**response.json()).node
            root_node_ids_to_delete.append(root_node.id)

        with allure.step('Проверка созданной компании'):
            expect(orgs_page.node_menu_button_place_locator_by_name(company_name),
                   f'Company {company_name} is missing on the page').to_have_count(1)

    @allure.id('133')
    @allure.title('Удаление компании')
    def test_delete_company(
            self,
            bff_client: BffApiClient,
            orgs_page: SettingsOrgTree,
            company_name: str,
            create_company: RootElem,
    ):
        with allure.step('Открыть меню действий компании'):
            orgs_page.node_menu_button_place_locator_by_name(company_name).click()

        with allure.step('Проверить локаторы контекстного меню'):
            orgs_page.check_specific_locators()

        with allure.step('Нажать на пункт удаления'):
            orgs_page.delete_node_menu_option.click()

            with orgs_page.expect_response(orgs_page.delete_node_request_lambda(
                    node_id=create_company.rootElem.id,
                    root_id=create_company.rootElem.id,
                    bff_client=bff_client)
            ) as resp_info:
                with allure.step('Открыто модальное окно подтверждения удаления'):
                    orgs_page.delete_form.check_specific_locators()

                with allure.step('Нажать на кнопку подтверждения'):
                    orgs_page.delete_form.confirm_button.click()

                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.NO_CONTENT)

        with allure.step('Компания отсутствует на странице'):
            expect(orgs_page.node_menu_button_place_locator_by_name(company_name),
                   f'Company {company_name} is still present on the page').to_have_count(0)
