from playwright.sync_api import Locator, expect, Page

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class OrgNodeEditForm(BasePage):
    def __init__(self, page: BasePage):
        super().__init__(page=page.page, page_url=page.page_url)

    @property
    def wrapper(self) -> Locator:
        return self.locator('div[class*="Drawer_Drawer__Container"]')

    @property
    def title(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Drawer_Drawer__Header")]]'
                            '/span[@class[contains(.,"Typography_header")]][contains(.,"Редактирование структуры")]')

    @property
    def close_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Drawer_Drawer__Header")]]'
                            '[span[@class[contains(.,"Typography_header")]]]/button')

    @property
    def cancel_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"EditNodeDrawer_Footer")]]/button[contains(.,"Отмена")]')

    @property
    def confirm_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"EditNodeDrawer_Footer")]]/button[contains(.,"Сохранить")]')

    @property
    def disabled_confirm_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"EditNodeDrawer_Footer")]]/button[contains(.,"Сохранить")]'
                            '[@disabled]')

    @property
    def name_input(self) -> Locator:
        return self.locator('//label[span[contains(.,"Наименование")]]/div/input')

    def check_specific_locators(self) -> None:
        expect(self.wrapper).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.title).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.close_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.cancel_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.confirm_button).to_be_visible(timeout=Timeouts.DEFAULT)
