from http import HTTPStatus

from core.clients.bff_api import BffApiClient
from core.helpers.utils import check_response_status
from core.models.tag import TagsResponse
from core.models.unit_nodes import UnitNodesResponse


def del_tags_for_node(client: BffApiClient, root_id: int, node_id: int):
    tags_resp = client.list_tags(root_id=root_id, node_id=node_id)
    check_response_status(given=tags_resp.status_code, expected=HTTPStatus.OK)
    tags = TagsResponse(**tags_resp.json()).list
    # Delete all tags
    for tag in tags:
        del_tag_resp = client.delete_tag(root_id=root_id, node_id=node_id, tag_uuid=tag.uuid)
        check_response_status(given=del_tag_resp.status_code, expected=HTTPStatus.NO_CONTENT)


def delete_unitnode(client: BffApiClient, root_id: int, node_id: int):
    # Obtain root node tree
    units_resp = client.list_unit_nodes_by_root_id(root_id=root_id)
    check_response_status(given=units_resp.status_code, expected=HTTPStatus.OK)
    nodes_dict = UnitNodesResponse(**units_resp.json()).nodes
    # Get node children
    children_ids = nodes_dict[str(node_id)].childrenIds
    # Delete all child nodes
    if children_ids:
        for child_id in children_ids:
            del_tags_for_node(client=client, root_id=root_id, node_id=child_id)
            # Delete node recursively
            delete_unitnode(client=client, root_id=root_id, node_id=child_id)
    del_node_resp = client.delete_unit_node(root_id=root_id, node_id=node_id)
    check_response_status(given=del_node_resp.status_code, expected=HTTPStatus.NO_CONTENT)
