import allure

from http import HTTPStatus
from playwright.sync_api import expect

from core.clients.bff_api import BffApiClient
from core.helpers.utils import check_response_status
from core.pages.settings_org_tree import SettingsOrgTree
from core.pages.unit_nodes_editor import UnitNodesEditor
from core.models.unit_marks import CreateUnitMarkResponse
from core.models.unit_nodes import CreateRootUnitNodeResponse, CreateUnitNodeResponse
from core.models.org_nodes import RootNodeResponse, CommonNode, NodeResponse
from core.models.tag import Tag, CreateTagResponse
from core.models.unit_type import CreateUnitTypeResponse


class TestOrgTreeUi:

    @allure.id('')
    @allure.title('Cоздание дерева организации')
    def test_org_tree_integration(self, orgs_page: SettingsOrgTree,
                                  front_url: str,
                                  bff_client: BffApiClient,
                                  root_org_node_name: str,
                                  second_root_org_node_name: str,
                                  child_org_node_name: str,
                                  unit_type_name: str,
                                  mark_name: str,
                                  child_unit_node_name: str,
                                  leaf_org_node_name: str,
                                  subchild_unit_node_name: str,
                                  temp_tag: Tag,
                                  unit_type_ids_to_delete: list,
                                  root_node_ids_to_delete: list):

        with allure.step('Открыта страница настроек дерева организации'):
            orgs_page.check_specific_locators()

        with allure.step('Нажать на кнопку добавления корневого элемента дерева'):
            orgs_page.add_tree_button.click()

        with allure.step('Открыта форма создания элемета орг.стуктуры'):
            orgs_page.create_form.check_specific_locators()

        with allure.step('Ввести название узла'):
            orgs_page.create_form.name_input.type(root_org_node_name)

        with allure.step('Нажать на кнопку "Добавить"'):
            root_node: CommonNode
            with orgs_page.expect_response(orgs_page.create_node_request_lambda(bff_client=bff_client)) as resp_info:
                orgs_page.create_form.confirm_button.click()
                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.CREATED)
                root_node = RootNodeResponse(**response.json()).node
            root_node_ids_to_delete.append(root_node.id)

        with allure.step('Добавленный элемент появился в списке узлов'):
            expect(orgs_page.node_locator_by_name(name=root_org_node_name)).to_be_visible()

        with allure.step('Открыть контекстное меню корневого элемента'):
            orgs_page.node_menu_button_place_locator_by_name(name=root_org_node_name).hover()
            orgs_page.node_menu_button_locator.click()

        with allure.step('Выбрать опцию "Редактировать"'):
            orgs_page.edit_node_menu_option.click()

        with allure.step('Открылась форма редактирования узла'):
            orgs_page.edit_form.check_specific_locators()

        with allure.step('Ввести новое название узла'):
            changed_name = f'{root_org_node_name} UPDATED'
            orgs_page.edit_form.name_input.clear()
            orgs_page.edit_form.name_input.type(changed_name)

        with allure.step('Нажать на кнопку сохранить'):
            orgs_page.edit_form.confirm_button.click()

        with allure.step('Форма редактирования закрыта'):
            orgs_page.wait_for_changes()
            expect(orgs_page.edit_form.wrapper).to_have_count(0)

        # FIXME: Uncomment steps below and remove closing editing form when fixed https://app.clickup.com/t/85zrz5twj
        # with allure.step('В списке узлов присутствует узел с изменённым названием'):
        #     expect(orgs_page.node_locator_by_name(name=changed_name)).to_be_visible()

        with allure.step('Нажать на кнопку добавления корневого элемента дерева'):
            orgs_page.add_tree_button.click()

        with allure.step('Открыта форма создания элемета орг.стуктуры'):
            orgs_page.create_form.check_specific_locators()

        with allure.step('Ввести название узла'):
            orgs_page.create_form.name_input.type(second_root_org_node_name)

        with allure.step('Нажать на кнопку "Добавить"'):
            second_root_node: CommonNode
            with orgs_page.expect_response(orgs_page.create_node_request_lambda(bff_client=bff_client)) as resp_info:
                orgs_page.create_form.confirm_button.click()
                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.CREATED)
                second_root_node = RootNodeResponse(**response.json()).node
            root_node_ids_to_delete.append(second_root_node.id)

        with allure.step('Добавленный элемент появился в списке узлов'):
            expect(orgs_page.node_locator_by_name(name=second_root_org_node_name)).to_be_visible()

        with allure.step('Нажать на название второго узла'):
            orgs_page.node_locator_by_name(name=second_root_org_node_name).click()

        with allure.step('Появился второй уровень структуры'):
            expect(orgs_page.level_2_column).to_be_visible()

        with allure.step('Нажать на кнопку "Добавить" второго уровня структуры'):
            orgs_page.lvl2_add_node_button.click()

        with allure.step('Открыта форма создания элемента структуры'):
            orgs_page.create_form.check_specific_locators()

        with allure.step('Ввести имя дочернего узла'):
            orgs_page.create_form.name_input.type(child_org_node_name)

        with allure.step('Нажать на кнопку "Добавить"'):
            child_node: CommonNode
            resp_lambda = orgs_page.create_child_node_request_lambda(root_id=second_root_node.id, bff_client=bff_client)

            with orgs_page.expect_response(resp_lambda) as resp_info:
                orgs_page.create_form.confirm_button.click()
                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.CREATED)
                child_node = NodeResponse(**response.json()).node

        with allure.step('Дочерний узел появился в списке узлов'):
            orgs_page.node_locator_by_name(name=child_org_node_name)

        with allure.step('Открыть страницу "Редактор узлов агрегата"'):
            unit_page = UnitNodesEditor(page=orgs_page.page, host=front_url)
            unit_page.visit()
            unit_page.wait_for_changes()
            unit_page.check_specific_locators()

        with allure.step('Открыть дропдаун оборудования'):
            unit_page.unit_dropdown.click()
            expect(unit_page.dropdown_wrapper).to_be_visible()

        with allure.step('Нажать на кнопку создания в дропдауне'):
            unit_page.dropdown_button.click()
            expect(unit_page.dropdown_input).to_be_visible()

        with allure.step('Ввести название типа оборудования и нажать Enter'):
            unit_page.dropdown_input.type(unit_type_name)
            with unit_page.expect_response(unit_page.create_unit_type_request_lambda(bff_client=bff_client)) \
                    as resp_info:
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

        with allure.step('Открыть дропдаун марок оборудования'):
            unit_page.empty_mark_dropdown.click()
            expect(unit_page.dropdown_wrapper).to_be_visible()

        with allure.step('Нажать на кнопку добавления марки'):
            unit_page.dropdown_button.click()
            expect(unit_page.dropdown_input).to_be_visible()

        with allure.step('Ввести название марки и нажать Enter'):
            unit_page.dropdown_input.type(mark_name)
            mark_id: int
            unit_root_id: int
            create_mark_resp = unit_page.create_mark_request_lambda(bff_client=bff_client)
            create_root_resp = unit_page.create_root_unit_node_request_lambda(bff_client=bff_client)
            with unit_page.expect_response(create_mark_resp) as mark_resp_info, \
                    unit_page.expect_response(create_root_resp) as root_resp_info:
                unit_page.page.keyboard.press('Enter')
                mark_resp = mark_resp_info.value
                check_response_status(given=mark_resp.status, expected=HTTPStatus.CREATED)
                mark_id = CreateUnitMarkResponse(**response.json()).unit_mark.id
                unit_resp = root_resp_info.value
                check_response_status(given=unit_resp.status, expected=HTTPStatus.CREATED)
                unit_root_id = CreateRootUnitNodeResponse(**unit_resp.json()).node.id

        with allure.step('Название марки появилось на странице'):
            expect(unit_page.dropdown_item_by_name(name=mark_name)).to_be_visible()

        with allure.step('Нажать на кнопку "Добавить узел"'):
            unit_page.add_node_button.click()

        with allure.step('В поле ввода ввести название и нажать Enter'):
            unit_page.new_node_name_input.type(child_unit_node_name)
            first_child_id: int
            with unit_page.expect_response(unit_page.create_unit_node_request_lambda(
                    bff_client=bff_client, node_id=unit_root_id)) as resp_info:
                unit_page.page.keyboard.press('Enter')
                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.CREATED)
                first_child_id = CreateUnitNodeResponse(**response.json()).node.id
                unit_page.wait_for_changes()

        with allure.step('Добавить к созданному узлу дочерний'):
            second_child_id: int
            unit_page.node_title_by_name(name=child_unit_node_name).hover()
            unit_page.create_subnode_button.click()
            unit_page.new_node_name_input.type(subchild_unit_node_name)
            with unit_page.expect_response(unit_page.create_unit_node_request_lambda(bff_client=bff_client,
                                                                                     node_id=first_child_id)) as resp_info:
                unit_page.page.keyboard.press('Enter')
                response = resp_info.value
                check_response_status(given=response.status, expected=HTTPStatus.CREATED)
                second_child_id = CreateUnitNodeResponse(**response.json()).node.id
                unit_page.wait_for_changes()

        with allure.step('Нажать на кнопку раскрытия дочерних узлов'):
            unit_page.wait(500)
            unit_page.expand_button_locator_by_node_name(name=child_unit_node_name).click()
            unit_page.wait_for_changes()

        with allure.step('Дочерний узел появился в списке'):
            expect(unit_page.node_title_by_name(name=subchild_unit_node_name)).to_be_visible()

        with allure.step('Нажать на кнопку добавления тега для дочернего узла'):
            unit_page.add_button_locator_by_node_name(name=subchild_unit_node_name).click()

        with allure.step('Открыт редактор тегов'):
            unit_page.add_tag.check_specific_locators()

        with allure.step('Нажать на кнопку добавления тега'):
            unit_page.add_tag.add_button.click()

        with allure.step('Заполнить форму данными тестового тега'):
            unit_page.add_tag.fill_form(tag=temp_tag)

        with allure.step('Нажать на кнопку "Сохранить"'):
            with unit_page.expect_response(unit_page.create_tag_request_lambda(bff_client=bff_client,
                                                                               root_id=unit_root_id,
                                                                               node_id=second_child_id)) as resp_info:
                unit_page.add_tag.save_button.click()
                response = resp_info.value
                # FIXME: BUG! Should be 201 (CREATED)
                check_response_status(given=response.status, expected=HTTPStatus.OK)
                tag_uuid = CreateTagResponse(**response.json()).tag.uuid

        with allure.step('Открыть страницу "Орг. структура"'):
            orgs_page.visit()
            orgs_page.check_specific_locators()

        with allure.step('Раскрыть дочерние узлы второго созданного корневого элемента'):
            orgs_page.node_locator_by_name(name=second_root_org_node_name).click()
            expect(orgs_page.level_2_column).to_be_visible()
            orgs_page.node_locator_by_name(name=child_org_node_name).click()
            expect(orgs_page.level_3_column).to_be_visible()

        with allure.step('Нажать на кнопку "Добавить" в колонке 3-го уновня'):
            orgs_page.lvl3_add_node_button.click()

        with allure.step('Открыта форма создания элемента структуры'):
            orgs_page.create_form.check_specific_locators()

        with allure.step('Ввести имя дочернего узла'):
            orgs_page.create_form.name_input.type(leaf_org_node_name)

        with allure.step('В дропдауне выбрать тип элемента "Агрегат"'):
            orgs_page.create_form.select_from_dropdown(dropdown=orgs_page.create_form.element_type_dropdown,
                                                       item=orgs_page.create_form.unit_dropdown_option)

        with allure.step('В дропдауне выбрать созданный вид оборудования'):
            orgs_page.create_form.select_from_dropdown(dropdown=orgs_page.create_form.unit_type_dropdown,
                                                       item=orgs_page.create_form.dropdown_option_by_name(
                                                           name=unit_type_name))

        with allure.step('Нажать на кнопку "Добавить"'):
            orgs_page.create_form.confirm_button.click()

        with allure.step('Добавленный тег присутствует на странице'):
            orgs_page.node_locator_by_name(name=leaf_org_node_name)
