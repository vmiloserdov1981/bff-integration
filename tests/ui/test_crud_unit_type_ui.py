from http import HTTPStatus

import allure
from playwright.sync_api import expect

from core.clients.bff_api import BffApiClient
from core.consts.timeouts import Timeouts
from core.helpers.utils import check_response_status
from core.models.unit_type import CreateUnitTypeResponse
from core.pages.unit_nodes_editor import UnitNodesEditor


class TestCRUDUnitType:

    @allure.id('213')
    @allure.title('Создание типа оборудования')
    def test_create_unit_type(self,
                              bff_client: BffApiClient,
                              mark_page: UnitNodesEditor,
                              unit_page: UnitNodesEditor,
                              unit_type_name: str,
                              unit_type_ids_to_delete: list):
        with allure.step('Открыть дропдаун типа оборудования'):
            unit_page.unit_dropdown.click()
            expect(unit_page.dropdown_wrapper).to_be_visible()

        with allure.step('Нажать на кнопку создания в дропдауне'):
            unit_page.dropdown_button.click()
            expect(unit_page.dropdown_input).to_be_visible()

        with allure.step('Ввести название типа оборудования и нажать Enter'):
            unit_page.dropdown_input.type(unit_type_name, timeout=Timeouts.TYPE_DELAY)
            with unit_page.expect_response(
                    unit_page.create_unit_type_request_lambda(bff_client=bff_client)) as resp_info:
                unit_page.page.keyboard.press('Enter')
                response = resp_info.value
                # FIXME: BUG! Should be 201 (CREATED)
                check_response_status(given=response.status, expected=HTTPStatus.OK)
                unit_type = CreateUnitTypeResponse(**response.json()).unit_type
                unit_type_ids_to_delete.append(unit_type.id)

        with allure.step('Тип оборудования присутствует в дропдауне'):
            expect(unit_page.dropdown_item_by_name(name=unit_type_name)).to_be_visible()

        with allure.step('Выбрать созданный тип оборудования'):
            unit_page.dropdown_item_by_name(name=unit_type_name).click()

        with allure.step('На странице присутствует пустое поле марки оборудования'):
            expect(unit_page.empty_mark_dropdown).to_be_visible()
