import allure
from http import HTTPStatus
from core.clients.bff_api import BffApiClient
from core.models.unit_marks import UnitMark
from core.models.unit_nodes import UnitNode
from core.models.unit_type import UnitType
from core.pages.settings_org_tree import SettingsOrgTree
from core.pages.unit_nodes_editor import UnitNodesEditor
from core.models.org_nodes import RootElem
from core.helpers.utils import check_response_status
from playwright.sync_api import expect


class TestAddUnit:
    @allure.id('137')
    @allure.title('Добавление агрегата')
    def test_add_unit(
        self,
        bff_client: BffApiClient,
        create_company: RootElem,
        existing_unit_type: UnitType,
        create_unit_mark: UnitMark,
        create_root_node_unit_api: UnitNode,
        orgs_page: SettingsOrgTree,
        unit_page: UnitNodesEditor,
        unit_name: str,
        unit_type_name: str,
        company_name: str,
        root_node_ids_to_delete: list,
        unit_type_ids_to_delete: list,
        existing_company: None
    ):
        with allure.step('Тестовая компания присутствует в списке компаний'):
            expect(
                orgs_page.node_locator_by_name(name=company_name),
                f'Locator by name {company_name} not found',
            ).to_have_count(1)

        with allure.step('Нажать на название созданной компании'):
            orgs_page.node_locator_by_name(name=company_name).click()

        with allure.step('Появился второй уровень структуры'):
            expect(orgs_page.level_2_column).to_be_visible()

        with allure.step('Нажать на кнопку "Добавить" второго уровня структуры'):
            orgs_page.lvl2_add_node_button.click()

        with allure.step('Открыта форма создания элемента структуры'):
            orgs_page.create_form.check_specific_locators()

        with allure.step('Ввести имя агрегата'):
            orgs_page.create_form.name_input.type(unit_name)

        with allure.step('В дропдауне выбрать тип элемента "Агрегат"'):
            orgs_page.create_form.select_from_dropdown(
                dropdown=orgs_page.create_form.element_type_dropdown,
                item=orgs_page.create_form.unit_dropdown_option,
            )

        with allure.step('В дропдауне выбрать созданный вид оборудования'):
            orgs_page.create_form.select_from_dropdown(
                dropdown=orgs_page.create_form.unit_type_dropdown,
                item=orgs_page.create_form.dropdown_option_by_name(name=unit_type_name),
            )
        with allure.step('Нажать на кнопку "Добавить"'):
            with orgs_page.expect_response(
                unit_page.create_child_node_request_lambda(
                    bff_client=bff_client, node_id=create_company.rootElem.id
                )
            ) as resp_info:
                orgs_page.create_form.confirm_button.click()
                response = resp_info.value
                check_response_status(
                    given=response.status, expected=HTTPStatus.CREATED
                )

        with allure.step('Добавленный агрегат присутствует на странице'):
            expect(
                orgs_page.node_locator_by_name(name=unit_name)
            ).to_have_count(1)
