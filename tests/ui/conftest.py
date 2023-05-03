import pytest

from playwright.sync_api import Page

from core.models.user import User
from core.pages.auth import AuthPage


@pytest.fixture(scope='session')
# TODO: move to env variable
def front_protocol() -> str:
    return 'http'


@pytest.fixture(scope='session')
# TODO: move to env variable
def front_host() -> str:
    return 'eryzhov.stages.c2g.pw'


@pytest.fixture(scope='session')
def main_page_url(front_protocol, front_host: str) -> str:
    return f'{front_protocol}://{front_host}'


@pytest.fixture(scope='function')
def main_page(page: Page, main_page_url: str) -> Page:
    page.goto(main_page_url)
    return page


@pytest.fixture(scope='function')
def auth_page(page: Page, front_host: str) -> AuthPage:
    auth = AuthPage(page=page, host=front_host)
    auth.visit()
    return auth
