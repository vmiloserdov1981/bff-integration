import allure
import pytest
from http import HTTPStatus
from playwright.sync_api import Page
from core.models.org_nodes import RootElem, RootNodeResponse, CommonNode
from core.clients.bff_api import BffApiClient
from core.helpers.utils import uniq_timestamp, check_response_status
from core.consts.timeouts import Timeouts
from core.models.user import User
from core.pages.auth import AuthPage
from core.pages.settings_org_tree import SettingsOrgTree


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
def company_name() -> str:
    return f'at_company{uniq_timestamp()}'


@pytest.fixture(scope='function')
def root_node_scaffold(company_name: str) -> RootElem:
    node = CommonNode(name=company_name)
    return RootElem(rootElem=node)


@pytest.fixture(scope='function')  # TODO: add deletion entity if not deleted by teardown
def create_company_api(bff_client: BffApiClient, company_name: str, root_node_scaffold: RootElem):
    request = bff_client.create_root_node(json=root_node_scaffold.body_for_creation)
    check_response_status(given=request.status_code, expected=HTTPStatus.CREATED)
    cr_resp_body = request.json()
    root_model_one = RootNodeResponse(**cr_resp_body).result
    return root_model_one
