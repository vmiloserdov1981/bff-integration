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
    def rules_locator(self) -> Locator:
        return self.locator('//*[@id="__next"]//*[text()="Правила"]')

    @property
    def create_rules_locator(self) -> Locator:
        return self.locator('//button[@class[contains(.,"Button_Button")]]//*[text()="Создать правило"]')

    def check_specific_locators(self) -> None:
        expect(self.rules_locator).to_be_visible(timeout=Timeouts.DEFAULT)

    @property
    def dropdown_choice_type_equipment(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Dropdown_Dropdown__Button")]]').first

    @property
    def choice_type_equipment(self) -> Locator:
        return self.locator('//div[contains(@class, "DropdownList_DropdownList") and .="A1"]')

    @property
    def dropdown_choice_brand(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Dropdown_Dropdown__Button")]]').last

    @property
    def choice_brand(self) -> Locator:
        return self.locator('//div[contains(@class, "DropdownList_DropdownList") and .="M2"]')

    @property
    def rule_name_locator(self) -> Locator:
        return self.locator('//label[span[contains(.,"Название")]]/input')

    @property
    def rule_description_locator(self) -> Locator:
        return self.locator('//label[span[contains(.,"Описание")]]/textarea')
