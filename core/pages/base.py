from typing import Callable
from playwright.sync_api import Locator, Page, expect
from core.consts.timeouts import Timeouts


class BasePage:

    def __init__(self, page: Page, page_url: str):
        self.page_url: str = page_url
        self.page: Page = page
        self.locator: Callable = self.page.locator
        self.wait = self.page.wait_for_timeout
        self.expect_response: Callable = self.page.expect_response

    def visit(self):
        self.page.goto(self.page_url)

    def wait_for_changes(self):
        self.page.wait_for_load_state(state='domcontentloaded')
        self.page.wait_for_load_state(state='networkidle')

    def select_from_dropdown(self, dropdown: Locator, item: Locator):
        dropdown.click()
        self.wait_for_changes()
        item.click()
        self.wait_for_changes()

    def check_locator_visibility(self, locator: Locator, timeout: float = Timeouts.DEFAULT) -> None:
        expect(locator).to_be_visible(timeout=timeout)
