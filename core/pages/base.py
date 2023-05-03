from playwright.sync_api import Page, Response, Locator
from typing import ContextManager

from core.consts.timeouts import Timeouts


class BasePage:
    def __init__(self, page: Page, url: str):
        self.url: str = url
        self.page: Page = page
        self.locator: Locator = self.page.locator
        self.wait = self.page.wait_for_timeout
        self.expect_response: ContextManager["Response"] = self.page.expect_response

    def visit(self):
        self.page.goto(self.url)
