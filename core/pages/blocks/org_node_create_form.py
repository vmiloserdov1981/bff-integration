from playwright.sync_api import Locator, expect, Page

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class OrgNodeCreateForm(BasePage):
    def __init__(self, page: BasePage):
        super().__init__(page=page.page, page_url=page.page_url)

    @property
    def wrapper(self) -> Locator:
        return self.locator('div[class*="Drawer_Drawer__Container"]')

    @property
    def title(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Drawer_Drawer__Header")]]'
                            '/span[@class[contains(.,"Typography_header")]][contains(.,"Новая структура")]')

    @property
    def close_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Drawer_Drawer__Header")]]'
                            '[span[@class[contains(.,"Typography_header")]]]/button')

    @property
    def cancel_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"CreateNodeDrawer_Footer")]]/button[contains(.,"Отмена")]')

    @property
    def confirm_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"CreateNodeDrawer_Footer")]]/button[contains(.,"Добавить")]')

    @property
    def disabled_confirm_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"CreateNodeDrawer_Footer")]]/button[contains(.,"Добавить")]'
                            '[@disabled]')

    @property
    def name_input(self) -> Locator:
        return self.locator('//label[span[contains(.,"Наименование")]]/div/input')

    @property
    def element_type_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    @property
    def unit_dropdown_option(self) -> Locator:
        return self.locator('//div[@class[contains(.,"DropdownList_DropdownList__Item")]][contains(.,"Агрегат")]')

    @property
    def unit_type_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Dropdown_Dropdown")]][span[contains(.,"Тип агрегата")]]'
                            '//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    def dropdown_option_by_name(self, name: str) -> Locator:
        return self.locator(f'//div[@class[contains(.,"DropdownList_DropdownList__Item")]][contains(.,"{name}")]')

    def check_specific_locators(self) -> None:
        expect(self.wrapper).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.title).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.close_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.cancel_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.confirm_button).to_be_visible(timeout=Timeouts.DEFAULT)
