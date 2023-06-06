from playwright.sync_api import Locator, Page, expect

from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class RulesCreateForm(BasePage):

    def __init__(self, page: BasePage):
        super().__init__(page=page.page, page_url=page.page_url)

    @property
    def start_frequency_dropdown(self) -> Locator:
        return self.locator('//div[span[contains(.,"Частота запуска")]]/div/div')

    def choice_start_frequency(self, name) -> Locator:
        return self.locator(f'//div[@class[contains(.,"DropdownList_DropdownList__Item")]][contains(.,"{name}")]/span')
