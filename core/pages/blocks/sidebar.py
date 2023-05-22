from playwright.sync_api import Locator, expect

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class SidebarMenu(BasePage):

    def __init__(self, page: BasePage):
        super().__init__(page=page.page, page_url=page.page_url)

    @property
    def org_tree_button(self) -> Locator:
        return self.locator('//a[@class[contains(.,"Navigation_Link")]][@href[contains(.,"/orgTree")]]')

    @property
    def mark_editor_button(self) -> Locator:
        return self.locator('//a[@class[contains(.,"Navigation_Link")]][@href[contains(.,"/markEditor")]]')

    @property
    def graphics_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Navigation_Link")]]/span[contains(.,Icon_icon)]').first

    @property
    def settings_button(self) -> Locator:
        return self.locator('//a[@class[contains(.,"Navigation_Link")]][@href[contains(.,"/settings")]]')

    @property
    def logout_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Navigation_Link")]]/span[contains(.,Icon_icon)]').last

    def check_specific_locators(self) -> None:
        expect(self.org_tree_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.mark_editor_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.graphics_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.settings_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.logout_button).to_be_visible(timeout=Timeouts.DEFAULT)
