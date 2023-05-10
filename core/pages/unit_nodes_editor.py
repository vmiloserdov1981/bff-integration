from playwright.sync_api import Page, Locator, expect

from typing import Callable

from core.clients.bff_api import BffApiClient
from core.consts.timeouts import Timeouts
from core.models.tag import Tag
from core.pages.base import BasePage
from core.pages.blocks.add_tag_form import AddTagForm


class UnitNodesEditor(BasePage):

    PATH = 'markEditor'

    def __init__(self, page: Page, host: str):
        super().__init__(page=page, page_url=f'{host}/{self.PATH}')
        self.title: str = 'Smart Diagnostics'
        self.add_tag = AddTagForm(page=self)

    @property
    def header_title(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Container_Container")]]'
                            '/span[contains(.,"Редактор узлов агрегата")]')

    @property
    def table_title(self):
        return self.locator('//div[@class[contains(.,"Table_TableCell")]]'
                            '/span[@class[contains(.,"Typography_subtitle")]][contains(.,"Вид оборудования")]')

    @property
    def add_node_button(self) -> Locator:
        return self.locator('//button[contains(.,"Добавить узел")]')

    @property
    def unit_dropdown(self) -> Locator:
        return self.locator('div[class*="Dropdown_Dropdown__Button"]').nth(0)

    @property
    def dropdown_wrapper(self) -> Locator:
        return self.locator('div[class*="Dropdown_Dropdown__Panel"]')

    @property
    def mark_dropdown(self) -> Locator:
        return self.locator('div[class*="Dropdown_Dropdown__Button"]').nth(1)

    @property
    def empty_mark_dropdown(self) -> Locator:
        return self.locator('//div[@class[contains(.,"Dropdown_Dropdown__Button")]]/span[@class'
                            '[contains(.,"Dropdown_Dropdown__Title__EIOZ_")]][contains(.,"Добавьте марку")]')

    @property
    def dropdown_button(self) -> Locator:
        return self.locator('//span[@class[contains(.,"EditingDropDown_DropDownListItem")]]')

    @property
    def dropdown_input(self) -> Locator:
        return self.locator('//input[@class[contains(.,"EditingDropDown_DropDownListItem")]]')

    def dropdown_item_by_name(self, name: str) -> Locator:
        return self.locator(f'//div[@class[contains(.,"SelectListItem_DropDownListItem")]]/span[contains(.,"{name}")]')

    def add_button_locator_by_node_name(self, name: str) -> Locator:
        return self.locator(f'//div[@class[contains(.,"Table_TableRow")]][div/div/span[contains(.,"{name}")]]'
                            f'//button[span[contains(.,"Добавить")]]')

    def expand_button_locator_by_node_name(self, name: str) -> Locator:
        return self.locator(f'//div[@class[contains(.,"Table_TableRow")]]'
                            f'[contains(.,"{name}")]/div/div/div/button').nth(0)

    @staticmethod
    def create_unit_type_url(bff_client: BffApiClient) -> str:
        return bff_client.unit_types_path()

    def create_unit_type_request_lambda(self, bff_client: BffApiClient) -> Callable:
        return lambda r: self.create_unit_type_url(bff_client=bff_client) in r.url and r.request.method == 'POST'
    
    @property
    def new_node_name_input(self) -> Locator:
        return self.locator('input[maxlength="80"][class*="EmptyNodeRow_Input"]')

    @property
    def edit_node_button(self) -> Locator:
        return self.locator('div[class*="UnitNodeComponent_NodeControls"]>button').nth(0)

    @property
    def create_subnode_button(self) -> Locator:
        return self.locator('div[class*="UnitNodeComponent_NodeControls"]>button').nth(1)

    def node_title_by_name(self, name: str) -> Locator:
        return self.locator(f'//div[@class[contains(.,"UnitNodeComponent_NodeWrapper")]]/span[contains(.,"{name}")]')

    @staticmethod
    def create_tag_request_url(bff_client: BffApiClient, root_id: int, node_id: int) -> str:
        return bff_client.tags_path(root_id=root_id, node_id=node_id)

    def create_tag_request_lambda(self, bff_client: BffApiClient, root_id: int, node_id: int) -> Callable:
        return lambda r: self.create_tag_request_url(bff_client=bff_client, root_id=root_id, node_id=node_id) in \
                         r.url and r.request.method == 'POST'

    @staticmethod
    def create_unit_node_request_url(bff_client: BffApiClient, node_id: int) -> str:
        return bff_client.unitnode_tree_children_path(node_id=node_id)

    def create_unit_node_request_lambda(self, bff_client: BffApiClient, node_id: int) -> Callable:
        return lambda r: self.create_unit_node_request_url(bff_client=bff_client,
                                                           node_id=node_id) in r.url and r.request.method == 'POST'

    @staticmethod
    def create_mark_request_url(bff_client: BffApiClient) -> str:
        return bff_client.unit_marks_path()

    def create_mark_request_lambda(self, bff_client: BffApiClient) -> Callable:
        return lambda r: self.create_mark_request_url(bff_client=bff_client) in r.url and r.request.method == 'POST'

    @staticmethod
    def create_root_unit_node_request_url(bff_client: BffApiClient) -> str:
        return bff_client.unitnode_trees_path()

    def create_root_unit_node_request_lambda(self, bff_client: BffApiClient) -> Callable:
        return lambda r: self.create_root_unit_node_request_url(bff_client=bff_client) in \
                         r.url and r.request.method == 'POST'

    def check_specific_locators(self) -> None:
        expect(self.header_title).to_be_visible(timeout=Timeouts.DEFAULT)
        # expect(self.table_title).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.add_node_button).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.unit_dropdown).to_be_visible(timeout=Timeouts.DEFAULT)
        expect(self.mark_dropdown).to_be_visible(timeout=Timeouts.DEFAULT)
