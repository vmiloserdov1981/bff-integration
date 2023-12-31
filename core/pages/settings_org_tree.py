from typing import Callable

from playwright.sync_api import Locator, Page, expect

from core.clients.bff_api import BffApiClient
from core.consts.timeouts import Timeouts
from core.pages.base import BasePage
from core.pages.blocks.org_node_create_form import OrgNodeCreateForm
from core.pages.blocks.org_node_delete_form import OrgNodeDeleteForm
from core.pages.blocks.org_node_edit_form import OrgNodeEditForm
from core.pages.blocks.sidebar import SidebarMenu


class SettingsOrgTree(BasePage):
    PATH = 'settings/org-tree'

    def __init__(self, page: Page, host: str):
        super().__init__(page=page, page_url=f'{host}/{self.PATH}')
        self.title: str = 'Smart Diagnostics'
        self.create_form = OrgNodeCreateForm(page=self)
        self.edit_form = OrgNodeEditForm(page=self)
        self.delete_form = OrgNodeDeleteForm(page=self)
        self.sidebar = SidebarMenu(page=self)

    @property
    def add_tree_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Column_Column")]][contains(.,"Уровень 1")]/div/button')

    @property
    def lvl2_add_node_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Column_Column")]][contains(.,"Уровень 2")]/div/button')

    @property
    def lvl3_add_node_button(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Column_Column")]][contains(.,"Уровень 3")]/div/button')

    @property
    def active_org_tree_tab(self) -> Locator:
        return self.locator('a[class*="NavigationBar_active"][href="/settings/org-tree"]')

    @property
    def users_tab(self) -> Locator:
        return self.locator('a[href="/settings/users"]')

    @property
    def roles_tab(self) -> Locator:
        return self.locator('a[href="/settings/roles"]')

    @staticmethod
    def create_node_request_url(bff_client: BffApiClient) -> str:
        return bff_client.org_trees_path()

    @staticmethod
    def delete_node_request_url(node_id: int, root_id: int, bff_client: BffApiClient) -> str:
        return bff_client.org_tree_node_path(node_id=node_id, root_id=root_id)

    def create_node_request_lambda(self, bff_client: BffApiClient) -> Callable:
        return lambda r: self.create_node_request_url(bff_client=bff_client) in r.url and r.request.method == 'POST'

    def delete_node_request_lambda(self, node_id: int, root_id: int, bff_client: BffApiClient) -> Callable:
        return lambda r: self.delete_node_request_url(node_id=node_id, root_id=root_id, bff_client=bff_client
                                                      ) in r.url and r.request.method == 'DELETE'

    @staticmethod
    def create_child_node_request_url(root_id: int, bff_client: BffApiClient) -> str:
        return bff_client.org_tree_child_nodes_path(node_id=root_id)

    def create_child_node_request_lambda(self, root_id: int, bff_client: BffApiClient) -> Callable:
        return (lambda r: self.create_child_node_request_url(root_id=root_id, bff_client=bff_client) in r.url and r.
                request.method == 'POST')

    def node_locator_by_name(self, name: str) -> Locator:
        return self.locator(f'//div[@class[contains(.,"Column_Content")]]/div[span[contains(.,"{name}")]]')

    def node_menu_button_place_locator_by_name(self, name: str) -> Locator:
        return self.locator(f'//div[@class[contains(.,"ColumnItem_clickable")]][span[contains(.,"{name}")]]'
                            f'/span[@class[contains(.,"Menu_Menu")]]')

    @property
    def node_menu_button_locator(self) -> Locator:
        return self.locator('//button[@class[contains(.,"ColumnItem_ActionIcon")]]')

    def unit_menu_button_locator(self, name) -> Locator:
        return self.locator(f'//div[@class[contains(.,"Column_Content")]]/div[span[contains(.,"{name}")]]//button')

    @property
    def edit_node_menu_option(self):
        return self.locator('//span[@class[contains(.,"MenuItem_md")]]/span[contains(.,"Редактировать")]')

    @property
    def delete_node_menu_option(self) -> Locator:
        return self.locator('//span[@class[contains(.,"MenuItem_md")]]/span[contains(.,"Удалить")]')

    @property
    def level_1_column(self):
        return self.locator('//div[@class[contains(.,"Column_Column")]]//span[contains(.,"Уровень 1")]')

    @property
    def level_2_column(self):
        return self.locator('//div[@class[contains(.,"Column_Column")]]//span[contains(.,"Уровень 2")]')

    @property
    def level_3_column(self):
        return self.locator('//div[@class[contains(.,"Column_Column")]]//span[contains(.,"Уровень 3")]')

    @property
    def turn_on_show_general_list_switch(self) -> Locator:
        return self.locator('//span[@class[contains(.,"Switch_Switch__Field")]]')

    @property
    def options_hide_from_the_list(self) -> Locator:
        return self.locator('//*[@id="__next"]//*[text()="Скрыть из общего списка"]')

    @property
    def options_show_from_the_list(self) -> Locator:
        return self.locator('//*[@id="__next"]//*[text()="Показать в общем списке"]')

    @property
    def locator_static_model(self) -> Locator:
        return self.locator('//*[@id="__next"]//*[text()="Стат. модель"]')

    def disclose_company_dropdown(self, name) -> Locator:
        return self.locator(
            f'//div[@class[contains(.,"py-2")]][contains(.,"{name}")]/parent::div/parent::div/div[@class[contains(.,"pl-3")]]/span'
        )

    def locator_entity_name(self, name) -> Locator:
        return self.locator(f'//div[@class[contains(.,"")]]//*[text()="{name}"]')

    def open_options_entity_1lv_2lv(self, name) -> Locator:
        return self.locator(f'//div[@class[contains(.,"ColumnItem_Container")]][contains(.,"{name}")]'
                            f'/span[@class[contains(.,"Menu_Menu")]]')

    @property
    def goto_monitoring_page(self) -> Locator:
        return self.locator(
            '#__next > div > div.MainLayout_NavigationLayout__8fojE > div.MainLayout_NavigationContainer__UuSmZ > div:nth-child(1) > span:nth-child(1) > a > span > svg > path'
        )

    def unit_in_general_list(self, name) -> Locator:
        return self.locator(f'//*[text()="{name}"]')

    def check_options_hide_from_the_list(self):
        expect(self.options_hide_from_the_list).to_be_visible()

    def check_options_show_from_the_list(self):
        expect(self.options_show_from_the_list).to_be_visible()

    def check_switcher_show_in_list_not_active(self):
        expect(self.options_show_from_the_list).to_have_count(0)

    def check_edit_unit(self):
        expect(self.edit_node_menu_option).to_have_count(1)

    def check_monitoring_page(self):
        expect(self.locator_static_model).to_have_count(1)

    def check_del_unit(self):
        expect(self.delete_node_menu_option).to_be_visible()

    def check_specific_locators(self) -> None:
        expect(self.page).to_have_title(self.title)
        expect(self.add_tree_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.active_org_tree_tab).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.users_tab).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.roles_tab).to_be_visible(timeout=Timeouts.DEFAULT)
