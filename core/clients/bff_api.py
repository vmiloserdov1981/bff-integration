import requests

from core.clients.base import BaseApiClient


class BffApiClient(BaseApiClient):

    def __init__(self, host: str, token: str = ''):
        super().__init__(token=token)
        self.host = host
        self.path_prefix = 'frontapi/v1'
        self.base_url = f'{self.host}/{self.path_prefix}'

    # PATHS
    def org_trees_path(self) -> str:
        return f'{self.path_prefix}/org-trees'

    def org_tree_node_path(self, root_id: int, node_id: int) -> str:
        return f'{self.path_prefix}/org-trees/{root_id}/nodes/{node_id}'

    def org_tree_child_nodes_path(self, node_id: int) -> str:
        return f'{self.path_prefix}/org-trees/{node_id}/nodes'

    def unit_types_path(self) -> str:
        return f'{self.path_prefix}/unit-types'

    def unit_type_path(self, type_id: int) -> str:
        return f'{self.path_prefix}/unit-types/{type_id}'

    def unitnode_trees_path(self) -> str:
        return f'{self.path_prefix}/unitnode-trees'

    def unitnode_tree_children_path(self, node_id: int) -> str:
        return f'{self.path_prefix}/unitnode-trees/{node_id}/nodes'

    def unitnode_tree_node_path(self, root_id: int, node_id: int) -> str:
        return f'{self.path_prefix}/unitnode-trees/{root_id}/nodes/{node_id}'

    def tags_path(self, root_id: int, node_id: int) -> str:
        return f'{self.path_prefix}/unitnode-trees/{root_id}/nodes/{node_id}/ltags'

    def tag_path(self, root_id: int, node_id: int, tag_uuid: str) -> str:
        return f'{self.path_prefix}/unitnode-trees/{root_id}/nodes/{node_id}/ltags/{tag_uuid}'

    def unit_marks_path(self) -> str:
        return f'{self.path_prefix}/unit-marks'

    def unit_mark_path(self, mark_id) -> str:
        return f'{self.path_prefix}/unit-marks/{mark_id}'

    # OrgNodes
    def list_org_trees(self, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.host}/{self.org_trees_path()}', params=params)

    def create_root_node(self, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.host}/{self.org_trees_path()}', json=json)

    def update_root_node(self, root_id: int, json: dict = None) -> requests.Response:
        return self.patch(url=f'{self.host}/{self.org_tree_node_path(root_id=root_id, node_id=root_id)}', json=json)

    def create_child_node(self, root_id: int, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.host}/{self.org_tree_child_nodes_path(node_id=root_id)}', json=json)

    def delete_root_node(self, root_id: int) -> requests.Response:
        return self.delete(url=f'{self.host}/{self.org_tree_node_path(root_id=root_id, node_id=root_id)}')

    def list_nodes_by_root_id(self, root_id: int, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.host}/{self.org_tree_child_nodes_path(node_id=root_id)}', params=params)

    def attach_unit_node(self, parent_id: int, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.host}/{self.org_tree_child_nodes_path(node_id=parent_id)}', json=json)

    # UNITS
    # Unit types

    def create_unit_type(self, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.host}/{self.unit_types_path()}', json=json)

    def delete_unit_type(self, type_id: int) -> requests.Response:
        return self.delete(url=f'{self.host}/{self.unit_type_path(type_id=type_id)}')

    # Unit nodes

    def create_root_unit_node(self, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.host}/{self.unitnode_trees_path()}', json=json)

    def create_unit_node(self, parent_id: int, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.host}/{self.unitnode_tree_children_path(node_id=parent_id)}', json=json)

    def list_unit_nodes_by_root_id(self, root_id: int, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.host}/{self.unitnode_tree_children_path(node_id=root_id)}', params=params)

    def delete_unit_node(self, root_id: int, node_id: int, json: dict = None) -> requests.Response:
        return self.delete(
            url=f'{self.host}/{self.unitnode_tree_node_path(root_id=root_id, node_id=node_id)}',
            json=json,
        )

    # Unit marks

    def create_unit_mark(self, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.host}/{self.unit_marks_path()}', json=json)

    def delete_unit_mark(self, mark_id: int, json: dict = None) -> requests.Response:
        return self.delete(url=f'{self.host}/{self.unit_mark_path(mark_id=mark_id)}', json=json)

    def list_unit_marks(self, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.host}/{self.unit_marks_path()}', params=params)

    # Tags

    def create_tag(self, root_id: int, node_id: int, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.host}/{self.tags_path(root_id=root_id, node_id=node_id)}', json=json)

    def list_tags(self, root_id: int, node_id: int, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.host}/{self.tags_path(root_id=root_id, node_id=node_id)}', params=params)

    def delete_tag(self, root_id: int, node_id: int, tag_uuid: str, json: dict = None) -> requests.Response:
        return self.delete(url=f'{self.host}/{self.tag_path(root_id=root_id, node_id=node_id, tag_uuid=tag_uuid)}',
                           json=json)
