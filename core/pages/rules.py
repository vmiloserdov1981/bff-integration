import typing

from playwright.sync_api import Locator, Page, expect

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class RulesPage(BasePage):
    PATH = 'rules'

    def __init__(self, page: Page, host: str):
        super().__init__(page=page, page_url=f'{host}/{self.PATH}')
        self.title: str = 'Smart Diagnostics'

    @property
    def org_structure_locator(self) -> Locator:
        return self.locator('//*[@id="__next"]//*[text()="Орг. структура"]')

    @property
    def create_rules_locator(self) -> Locator:
        return self.locator('//button[@class[contains(.,"Button_Button")]]//*[text()="Создать правило"]')

    def check_specific_locators(self) -> None:
        expect(self.org_structure_locator).to_be_visible(timeout=Timeouts.DEFAULT)
