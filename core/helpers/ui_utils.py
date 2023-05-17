from playwright.sync_api import Locator

from core.pages.base import BasePage


# FIXME: Compare with BasePage method
def dropdown_select(page: BasePage, dropdown: Locator, item: Locator):
    dropdown.click()
    page.wait_for_changes()
    item.click()
    page.wait_for_changes()
