from http import HTTPStatus

import allure
from playwright.sync_api import expect

from core.clients.bff_api import BffApiClient
from core.consts.timeouts import Timeouts
from core.helpers.utils import check_response_status
from core.models.unit_nodes import CreateUnitNodeResponse, UnitNode
from core.pages.settings_org_tree import SettingsOrgTree
from core.pages.unit_nodes_editor import UnitNodesEditor


class TestCRUDUnitNode:

    @allure.id('230')
    @allure.title('Создание узла и подузла оборудования')
    def test_create_unit_node(
        self,
        front_url: str,
        bff_client: BffApiClient,
        orgs_page: SettingsOrgTree,
        unit_page: UnitNodesEditor,
        unit_type_name: str,
        unit_mark_name: str,
        child_unit_node_name: str,
        subchild_unit_node_name: str,
        create_root_node_unit: UnitNode,
    ):
        with allure.step('Открыта страница "Шаблоны видов"'):
            unit_page.check_specific_locators()

        with allure.step('Открыть дропдаун оборудования и выбрать оборудование'):
            unit_page.unit_dropdown.click()
            expect(unit_page.dropdown_wrapper).to_be_visible()
            unit_page.dropdown_item_by_name(name=unit_type_name).click()

        with allure.step('Открыть дропдаун марок оборудования и выбрать марку'):
            unit_page.mark_dropdown.click()
            expect(unit_page.dropdown_wrapper).to_be_visible()
            unit_page.dropdown_item_by_name(name=unit_mark_name).click()

        with allure.step('Нажать на кнопку "Добавить узел"'):
            unit_page.add_node_button.click()

        with allure.step('В поле ввода ввести название узла и нажать Enter'):
            unit_page.new_node_name_input.type(child_unit_node_name)
            first_child_id: int
            with unit_page.expect_response(
                    unit_page.create_unit_node_request_lambda(bff_client=bff_client,
                                                              node_id=create_root_node_unit.id)) as resp_info:
                unit_page.page.keyboard.press('Enter')
                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.CREATED)
                first_child_id = CreateUnitNodeResponse(**response.json()).node.id
                unit_page.wait_for_changes()

        with allure.step('Выбрать созданный узел'):
            unit_page.node_title_by_name(name=child_unit_node_name).hover()
            unit_page.create_subnode_button.click()

        with allure.step('Добавить к созданному узлу дочерний узел и нажать Enter'):
            unit_page.new_node_name_input.type(subchild_unit_node_name)
            # TODO LATER:
            # second_child_id: int
            with unit_page.expect_response(
                    unit_page.create_unit_node_request_lambda(bff_client=bff_client,
                                                              node_id=first_child_id)) as resp_info:
                unit_page.page.keyboard.press('Enter')
                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.CREATED)
                # TODO LATER:
                # second_child_id = CreateUnitNodeResponse(**response.json()).node.id
                unit_page.wait_for_changes()

        with allure.step('Нажать на кнопку раскрытия дочерних узлов'):
            # TODO: figure out, why should we use timeout here
            unit_page.wait(timeout=Timeouts.SUBCHILD_NODE_OPEN)
            unit_page.expand_button_locator_by_node_name(name=child_unit_node_name).click()
            unit_page.wait_for_changes()

        with allure.step('Дочерний узел появился в списке'):
            expect(unit_page.node_title_by_name(name=subchild_unit_node_name)).to_be_visible()
