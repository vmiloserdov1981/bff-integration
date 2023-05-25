from playwright.sync_api import Locator, expect
from core.consts.timeouts import Timeouts
from core.pages.base import BasePage


class OrgNodeDeleteForm(BasePage):

    def __init__(self, page: BasePage):
        super().__init__(page=page.page, page_url=page.page_url)

    @property
    def wrapper(self) -> Locator:
        return self.locator('div[role="dialog"]')

    @property
    def close_button(self) -> Locator:
        return self.locator('[role="dialog"] [class*="IconButton_IconButton"]')

    @property
    def cancel_button(self) -> Locator:
        return self.locator('[role="dialog"] button:nth-child(1)')

    @property
    def confirm_button(self) -> Locator:
        return self.locator('[role="dialog"] [class*="Button_error"]')

    @property
    def title_confirmation_modal(self) -> Locator:
        return self.locator('//span[contains(.,"Вы уверены, что хотите удалить структуру?")]')

    @property
    def description_confirmation_modal(self) -> Locator:
        return self.locator('//span[contains(.,"Данное действие не может быть отменено")]')

    def check_specific_locators(self) -> None:
        expect(self.wrapper).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.close_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.cancel_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.confirm_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.title_confirmation_modal).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.description_confirmation_modal).to_be_visible(timeout=Timeouts.DEFAULT)
