from playwright.sync_api import Locator

from core.pages.base import BasePage


def dropdown_select(page: BasePage, dropdown: Locator, item: Locator):
    dropdown.click()
    page.wait_for_changes()
    item.click()
    page.wait_for_changes()
