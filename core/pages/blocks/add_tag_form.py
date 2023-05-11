from typing import Callable

from playwright.sync_api import Locator, Page, expect

from core.consts.timeouts import Timeouts
from core.helpers.ui_utils import dropdown_select
from core.models.physical_quantity import physical_quantity
from core.models.tag import Tag
from core.pages.base import BasePage


class AddTagForm(BasePage):

    def __init__(self, page: BasePage):
        super().__init__(page=page.page, page_url=page.page_url)

    @property
    def form_title(self) -> Locator:
        return self.locator('//span[contains(.,"Редактор тегов")]')

    @property
    def add_button(self) -> Locator:
        return self.locator('//button/span[contains(.,"Добавить тег")]')

    @property
    def cancel_button(self) -> Locator:
        return self.locator('//button/span[contains(.,"Отмена")]')

    @property
    def save_button(self) -> Locator:
        return self.locator('//button/span[contains(.,"Сохранить")]')

    @property
    def delete_button(self) -> Locator:
        return self.locator('div[class*="EditorDrawer_Data__Button"]>button')

    @property
    def close_button(self) -> Locator:
        return self.locator('div[class*="Drawer_Drawer__Header"]>button')

    @property
    def title(self) -> Locator:
        return self.locator('//label[span[contains(.,"Наименование тега")]]/textarea')

    @property
    def physical_quantity_dropdown(self) -> Locator:
        return self.locator('//div[span[contains(.,"Физическая величина")]]'
                            '//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    def dropdown_item_by_name(self, name: str) -> Locator:
        return self.locator(f'//div[@class[contains(.,"DropdownList_DropdownList__Item")]]/span[contains(.,"{name}")]')

    @property
    def observable_checkbox(self) -> Locator:
        return self.locator('//label[span[contains(.,"Отображать на экране флотатора")]]/input')

    @property
    def operating_range_upper_checkbox(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Верхняя граница")]]//input[@type="checkbox"]')

    @property
    def operating_range_upper_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Верхняя граница")]]//input[@type="number"]')

    @property
    def operating_range_lower_checkbox(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Нижняя граница")]]//input[@type="checkbox"]')

    @property
    def operating_range_lower_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Нижняя граница")]]//input[@type="number"]')

    @property
    def upper_first_threshold_checkbox(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]]'
                            '[span[contains(.,"Верхние пороги")]]//label[contains(.,"Первый порог")]/input')

    @property
    def upper_first_threshold_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Верхние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Первый порог")]]//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    @property
    def upper_first_threshold_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Верхние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Первый порог")]]//input[@type="number"]')

    @property
    def upper_second_threshold_checkbox(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]]'
                            '[span[contains(.,"Верхние пороги")]]//label[contains(.,"Второй порог")]/input')

    @property
    def upper_second_threshold_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Верхние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Второй порог")]]//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    @property
    def upper_second_threshold_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Верхние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Второй порог")]]//input[@type="number"]')

    @property
    def upper_third_threshold_checkbox(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]]'
                            '[span[contains(.,"Верхние пороги")]]//label[contains(.,"Третий порог")]/input')

    @property
    def upper_third_threshold_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Верхние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Третий порог")]]//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    @property
    def upper_third_threshold_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Верхние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Третий порог")]]//input[@type="number"]')

    @property
    def lower_first_threshold_checkbox(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]]'
                            '[span[contains(.,"Нижние пороги")]]//label[contains(.,"Первый порог")]/input')

    @property
    def lower_first_threshold_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Нижние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Первый порог")]]//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    @property
    def lower_first_threshold_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Нижние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Первый порог")]]//input[@type="number"]')

    @property
    def lower_second_threshold_checkbox(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]]'
                            '[span[contains(.,"Нижние пороги")]]//label[contains(.,"Второй порог")]/input')

    @property
    def lower_second_threshold_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Нижние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Второй порог")]]//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    @property
    def lower_second_threshold_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Нижние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Второй порог")]]//input[@type="number"]')

    @property
    def lower_third_threshold_checkbox(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]]'
                            '[span[contains(.,"Нижние пороги")]]//label[contains(.,"Третий порог")]/input')

    @property
    def lower_third_threshold_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Нижние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Третий порог")]]//div[@class[contains(.,"Dropdown_Dropdown__Button")]]')

    @property
    def lower_third_threshold_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]][contains(.,"Нижние пороги")]'
                            '//div[@class[contains(.,"AttributeItem_AttributeItem")]]'
                            '[div[@class[contains(.,"AttributeItem_AttributeItem__Title")]]'
                            '[contains(.,"Третий порог")]]//input[@type="number"]')

    @property
    def upper_display_range_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]]'
                            '[span[contains(.,"Порог отображения")]]//input[@type="number"]').nth(0)

    @property
    def lower_display_range_input(self) -> Locator:
        return self.locator('//div[@class[contains(.,"AttributeGroup_AttributeGroup")]]'
                            '[span[contains(.,"Порог отображения")]]//input[@type="number"]').nth(1)

    def fill_form(self, tag: Tag):
        self.title.type(tag.title)
        dropdown_select(page=self,
                        dropdown=self.physical_quantity_dropdown,
                        item=self.dropdown_item_by_name(name=physical_quantity.get(tag.physicalQuantity)))
        # if tag.markedAsObservable:
        #     self.observable_checkbox.click()
        if tag.operatingRange.upper.isActive:
            self.operating_range_upper_input.click()
            self.wait_for_changes()
            self.operating_range_upper_input.type(str(tag.operatingRange.upper.value))
        if tag.operatingRange.lower.isActive:
            self.operating_range_lower_input.click()
            self.wait_for_changes()
            self.operating_range_lower_input.type(str(tag.operatingRange.lower.value))
        # FIXME: Some hardcode here. Rewrite accurately
        # Fill upper low threshold (so it used in fixture now)
        self.upper_first_threshold_input.click()
        self.upper_first_threshold_input.type(tag.first_upper_active.str_value)

        # Fill lower urgent threshold (same reason)
        self.lower_second_threshold_input.click()
        self.lower_second_threshold_input.type(tag.first_lower_active.str_value)

        # Fill upper display range
        self.upper_display_range_input.click()
        self.upper_display_range_input.type(tag.displayRange.upper.str_value)

        # Fill lower display range
        self.lower_display_range_input.click()
        self.lower_display_range_input.type(tag.displayRange.lower.str_value)

    def check_specific_locators(self) -> None:
        expect(self.form_title).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.add_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.close_button).to_be_visible(timeout=Timeouts.DEFAULT)
