import allure
from http import HTTPStatus
from core.pages.settings_org_tree import SettingsOrgTree
from core.consts.timeouts import Timeouts
from core.models.org_nodes import CommonNode, RootNodeResponse
from core.helpers.utils import check_response_status
from core.clients.bff_api import BffApiClient


class TestCreateCompany:

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
            orgs_page.wait(timeout=Timeouts.COMPANY_CREATION)  # FIXME: replace for event waiting
            assert orgs_page.last_company_in_list.last.text_content() == company_name, \
                f'Name of last elem in company list is not equal created one'
