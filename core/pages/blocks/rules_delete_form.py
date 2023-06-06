from playwright.sync_api import Locator, Page, expect

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class RulesDeleteForm(BasePage):

    def __init__(self, page: BasePage):
        super().__init__(page=page.page, page_url=page.page_url)

    @property
    def confirm_button(self) -> Locator:
        return self.locator('//span[contains(@class, "Button_Button") and .="Ок"]')
