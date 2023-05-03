import requests


from core.clients.base import BaseApiClient


class BffApiClient(BaseApiClient):
    def __init__(self, host: str, token: str = ''):
        super().__init__(token=token)
        self.host = host
        self.path_prefix = 'frontapi/v1'
        self.base_url = f'{self.host}/{self.path_prefix}'

    # OrgNodes
    def list_org_trees(self, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.base_url}/org-trees', params=params)

    def create_root_node(self, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.base_url}/org-trees', json=json)

    def update_root_node(self, root_id: int, json: dict = None) -> requests.Response:
        return self.patch(url=f'{self.base_url}/org-trees/{root_id}/nodes/{root_id}', json=json)

    def create_child_node(self, root_id: int, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.base_url}/org-trees/{root_id}/nodes', json=json)

    def delete_root_node(self, root_id: int) -> requests.Response:
        return self.delete(url=f'{self.base_url}/org-trees/{root_id}/nodes/{root_id}')

    def list_nodes_by_root_id(self, root_id: int, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.base_url}/org-trees/{root_id}/nodes', params=params)

    def attach_unit_node(self, parent_id: int, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.base_url}/org-trees/{parent_id}/nodes', json=json)

    # UNITS
    # Unit types

    def create_unit_type(self, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.base_url}/unit-types', json=json)

    def delete_unit_type(self, type_id: int) -> requests.Response:
        return self.delete(url=f'{self.base_url}/unit-types/{type_id}')

    # Unit nodes

    def create_root_unit_node(self, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.base_url}/unitnode-trees', json=json)

    def create_unit_node(self, parent_id: int, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.base_url}/unitnode-trees/{parent_id}/nodes', json=json)

    def list_unit_nodes_by_root_id(self, root_id: int, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.base_url}/unitnode-trees/{root_id}/nodes', params=params)

    def delete_unit_node(self, root_id: int, node_id: int, json: dict = None) -> requests.Response:
        return self.delete(url=f'{self.base_url}/unitnode-trees/{root_id}/nodes/{node_id}', json=json)

    # Unit marks

    def create_unit_mark(self, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.base_url}/unit-marks', json=json)

    def delete_unit_mark(self, mark_id: int, json: dict = None) -> requests.Response:
        return self.delete(url=f'{self.base_url}/unit-marks/{mark_id}', json=json)

    def list_unit_marks(self, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.base_url}/unit-marks', params=params)

    # Tags

    def create_tag(self, root_id: int, node_id: int, json: dict = None) -> requests.Response:
        return self.post(url=f'{self.base_url}/unitnode-trees/{root_id}/nodes/{node_id}/ltags', json=json)

    def list_tags(self, root_id: int, node_id: int, params: dict = None) -> requests.Response:
        return self.get(url=f'{self.base_url}/unitnode-trees/{root_id}/nodes/{node_id}/ltags', params=params)

    def delete_tag(self, root_id: int, node_id: int, tag_uuid: str, json: dict = None) -> requests.Response:
        return self.delete(url=f'{self.base_url}/unitnode-trees/{root_id}/nodes/{node_id}/ltags/{tag_uuid}', json=json)
