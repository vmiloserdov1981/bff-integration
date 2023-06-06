import typing

from playwright.sync_api import Locator, Page, expect

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage
from core.pages.blocks.rules_create_form import RulesCreateForm
from core.pages.blocks.rules_delete_form import RulesDeleteForm
from core.pages.blocks.sidebar import SidebarMenu


class RulesPage(BasePage):
    PATH = 'rules'

    def __init__(self, page: Page, host: str):
        super().__init__(page=page, page_url=f'{host}/{self.PATH}')
        self.title: str = 'Smart Diagnostics'
        self.create_form = RulesCreateForm(page=self)
        self.delete_form = RulesDeleteForm(page=self)
        self.sidebar = SidebarMenu(page=self)

    @property
    def rules_locator(self) -> Locator:
        return self.locator('//*[@id="__next"]//*[text()="Правила"]')

    @property
    def create_rules_locator(self) -> Locator:
        return self.locator('//button[@class[contains(.,"Button_Button")]]//*[text()="Создать правило"]')

    @property
    def save_rules_btn(self) -> Locator:
        return self.locator('//button[@class[contains(.,"Button_Button")]]//*[text()="Сохранить"]')

    def check_specific_locators(self) -> None:
        expect(self.rules_locator).to_be_visible(timeout=Timeouts.DEFAULT)

    @property
    def dropdown_choice_type_equipment(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Dropdown_Dropdown__Button")]]').first

    def choice_type_equipment(self, name) -> Locator:
        return self.locator(f'//div[contains(@class, "DropdownList_DropdownList") and .="{name}"]')

    @property
    def dropdown_choice_brand(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Dropdown_Dropdown__Button")]]').last

    def choice_brand(self, name) -> Locator:
        return self.locator(f'//div[contains(@class, "DropdownList_DropdownList") and .="{name}"]').last

    @property
    def rule_name_locator(self) -> Locator:
        return self.locator('//label[span[contains(.,"Название")]]/input')

    @property
    def rule_description_locator(self) -> Locator:
        return self.locator('//label[span[contains(.,"Описание")]]/textarea')

    @property
    def start_frequency_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Dropdown_Dropdown__Button")]][contains(.,"Каждые 10 секунд")]')

    def choice_start_frequency(self, name) -> Locator:
        return self.locator(f'//div[@class[contains(.,"DropdownList_DropdownList__Item")]][contains(.,"{name}")]/span')

    def check_rule_display(self, name) -> Locator:
        return self.locator(f'//span[@class[contains(.,"Typography_Typography")]][contains(.,"{name}")]')

    @property
    def delete_rule_btn(self) -> Locator:
        return self.locator(
            '(//div[@class[contains(.,"Table_TableRow")]][contains(.,"1234")]//button[@class[contains(.,"IconButton_clear")]])[3]'
        )
