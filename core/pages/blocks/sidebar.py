from playwright.sync_api import Locator, expect

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class SidebarMenu(BasePage):

    def __init__(self, page: BasePage):
        super().__init__(page=page.page, page_url=page.page_url)

    @property
    def logout_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Navigation_Link")]]/span[contains(.,Icon_icon)]').last

    def check_specific_locators(self) -> None:
        expect(self.logout_button).to_be_visible(timeout=Timeouts.DEFAULT)
