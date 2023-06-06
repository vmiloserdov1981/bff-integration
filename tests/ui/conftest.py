from http import HTTPStatus

import allure
import pytest
from playwright.sync_api import Page

from core.clients.bff_api import BffApiClient
from core.consts.timeouts import Timeouts
from core.helpers.utils import check_response_status, uniq_timestamp
from core.models.org_nodes import AttachedNode, AttachNodeResponse, CommonNode, RootElem, RootNodeResponse
from core.models.unit_marks import CreateUnitMarkResponse, UnitMark
from core.models.unit_nodes import CreateRootUnitNodeResponse, UnitNode
from core.models.unit_type import CreateUnitTypeResponse, UnitType
from core.models.user import User
from core.pages.auth import AuthPage
from core.pages.settings_org_tree import SettingsOrgTree
from core.pages.unit_nodes_editor import UnitNodesEditor

pytest_plugins = ('core.plugins.snapshot', )


@pytest.fixture(scope='session')
def front_protocol(stand_params: dict) -> str:
    protocol = stand_params.get('protocol')
    return protocol


@pytest.fixture(scope='session')
def front_host(env_name: str) -> str:
    return f'{env_name}.stages.c2g.pw'


@pytest.fixture(scope='session')
def front_url(front_protocol: str, front_host: str) -> str:
    return f'{front_protocol}://{front_host}'


@pytest.fixture(scope='session')
def main_page_url(front_url: str) -> str:
    return front_url


@pytest.fixture(scope='function')
def main_page(page: Page, main_page_url: str) -> Page:
    page.goto(main_page_url)
    return page


@pytest.fixture(scope='function')
def auth_page(page: Page, front_url: str) -> AuthPage:
    auth = AuthPage(page=page, host=front_url)
    auth.visit()
    return auth


@pytest.fixture(scope='function')
def logged_page(default_user: User, auth_page: AuthPage) -> Page:
    with allure.step('Открыта страница логина'):
        auth_page.check_specific_locators()

    with allure.step('Ввести логин пользователя'):
        auth_page.login_input.type(text=default_user.login, timeout=Timeouts.DEFAULT)

    with allure.step('Ввести пароль пользователя'):
        auth_page.password_input.type(text=default_user.password, timeout=Timeouts.DEFAULT)

    with allure.step('Нажать на кнопку Войти'):
        with auth_page.expect_response(auth_page.session_response_lambda) as response_info:
            auth_page.submit_button.click(timeout=Timeouts.DEFAULT)
            response = response_info.value

    with allure.step('Session request returns 200'):
        assert (response.status == HTTPStatus.OK), f'Expecting status OK, got {response.status} instead'

    return auth_page.page


@pytest.fixture(scope='function')
def orgs_page(logged_page: Page, front_url: str) -> SettingsOrgTree:
    settings_page = SettingsOrgTree(page=logged_page, host=front_url)
    settings_page.visit()
    return settings_page


@pytest.fixture(scope='function')
def mark_page(logged_page: Page, front_url: str) -> UnitNodesEditor:
    marks_page = UnitNodesEditor(page=logged_page, host=front_url)
    marks_page.visit()
    return marks_page


@pytest.fixture(scope='function')
def unit_page(logged_page: Page, front_url: str) -> UnitNodesEditor:
    unit_page = UnitNodesEditor(page=logged_page, host=front_url)
    unit_page.visit()
    return unit_page


@pytest.fixture(scope='function')
def company_name() -> str:
    return f'at_company{uniq_timestamp()}'


@pytest.fixture(scope='function')
def unit_name() -> str:
    return f'at_unit{uniq_timestamp()}'


@pytest.fixture(scope='function')
def unit_type_name() -> str:
    return f'at_unit_type{uniq_timestamp()}'


@pytest.fixture(scope='function')
def unit_type_name_edited() -> str:
    return f'at_unit_type{uniq_timestamp()}_upd'


@pytest.fixture(scope='function')
def unit_mark_name() -> str:
    return f'at_unit_mark{uniq_timestamp()}'


@pytest.fixture(scope='function')
def root_unit_node_name() -> str:
    return f'at_root_unit_node{uniq_timestamp()}'


@pytest.fixture(scope='function')
def root_node_scaffold(company_name: str) -> RootElem:
    node = CommonNode(name=company_name)
    return RootElem(rootElem=node)


@pytest.fixture(scope='function')  # TODO: add deletion entity if not deleted by teardown
def create_company(bff_client: BffApiClient, company_name: str, root_node_scaffold: RootElem,
                   root_node_ids_to_delete: list):
    request = bff_client.create_root_node(json=root_node_scaffold.body_for_creation)
    check_response_status(given=request.status_code, expected=HTTPStatus.CREATED)
    cr_resp_body = request.json()
    root_model_one = RootNodeResponse(**cr_resp_body).result
    return root_model_one


@pytest.fixture(scope='function')
def existing_company(create_company: RootElem, root_node_ids_to_delete: list) -> None:
    root_node_ids_to_delete.append(create_company.rootElem.id)


@pytest.fixture(scope='function')
def existing_unit_type(bff_client: BffApiClient, unit_type_scaffold: UnitType,
                       unit_type_ids_to_delete: list) -> UnitType:
    create_ut_resp = bff_client.create_unit_type(json=unit_type_scaffold.body_for_creation)
    # TODO: Report bug 200 isn't normal for creation. Should be 201
    check_response_status(given=create_ut_resp.status_code, expected=HTTPStatus.OK)
    unit_type = CreateUnitTypeResponse(**create_ut_resp.json()).unit_type
    type_id = unit_type.id
    unit_type_ids_to_delete.append(type_id)
    return unit_type


@pytest.fixture(scope='function')
def create_unit_mark(
    bff_client: BffApiClient,
    existing_unit_type: UnitType,
    unit_mark_name: str,
) -> UnitMark:
    create_mark_resp = bff_client.create_unit_mark(
        json=UnitMark(name=unit_mark_name, typeId=existing_unit_type.id).dict(exclude_unset=True))
    check_response_status(given=create_mark_resp.status_code, expected=HTTPStatus.CREATED)
    unit_mark = CreateUnitMarkResponse(**create_mark_resp.json()).unit_mark
    return unit_mark


@pytest.fixture(scope='function')
def create_root_node_unit(bff_client: BffApiClient, existing_unit_type: UnitType, create_unit_mark: UnitMark,
                          root_unit_node_name: str) -> UnitNode:
    root_node_scaffold = UnitNode(name=root_unit_node_name,
                                  typeId=existing_unit_type.id,
                                  markId=create_unit_mark.id,
                                  unitKind='UNIT_NODE')
    create_root_unit_resp = bff_client.create_root_unit_node(json=root_node_scaffold.body_for_root_creation)
    check_response_status(given=create_root_unit_resp.status_code, expected=HTTPStatus.CREATED)
    root_unit_node = CreateRootUnitNodeResponse(**create_root_unit_resp.json()).node
    return root_unit_node


@pytest.fixture(scope='function')
def link_unit_to_node(bff_client: BffApiClient, create_company: RootElem, unit_name: str,
                      create_root_node_unit: UnitNode) -> AttachedNode:
    attachable_node = CommonNode(name=unit_name,
                                 parentId=create_company.rootElem.id,
                                 unitNodeTreeRootIdRef=create_root_node_unit.id)
    link_template_resp = bff_client.attach_unit_node(parent_id=create_company.rootElem.id,
                                                     json=attachable_node.body_for_creation)
    check_response_status(given=link_template_resp.status_code, expected=HTTPStatus.CREATED)
    # TODO: Check for 'status' and 'visibility' PATCH requests
    linked_node = AttachNodeResponse(**link_template_resp.json()).node
    return linked_node


@pytest.fixture(scope='function')
def child_unit_node_name() -> str:
    return f'child_node_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def subchild_unit_node_name() -> str:
    return f'subchild_node_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def unit_type_scaffold(unit_type_name: str) -> UnitType:
    return UnitType(name=unit_type_name)


@pytest.fixture(scope='function')
def mark_name() -> str:
    return f'mark_{uniq_timestamp()}'
