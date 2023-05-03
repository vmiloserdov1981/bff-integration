import pytest

from http import HTTPStatus

from core.clients.auth_api import AuthApiClient
from core.clients.bff_api import BffApiClient
from core.helpers.utils import check_response_status
from core.models.user import User
from core.models.unit_marks import UnitMark, UnitMarksListResponse
from core.models.unit_nodes import UnitNodesResponse
from core.models.tag import TagsResponse


@pytest.fixture(scope='session')
def env_name() -> str:
    # TODO: Move to env variables
    return 'eryzhov'


@pytest.fixture(scope='session')
def auth_host(env_name: str) -> str:
    return f'http://authapi.{env_name}.stages.c2g.pw'


@pytest.fixture(scope='session')
def bff_host(env_name: str) -> str:
    return f'http://{env_name}.stages.c2g.pw'


@pytest.fixture(scope='session')
def default_user() -> User:
    user = User(login='testuser', password='testuser')
    return user


@pytest.fixture(scope='function')
def auth_client(auth_host: str) -> AuthApiClient:
    client = AuthApiClient(host=auth_host)
    return client


@pytest.fixture(scope='function')
def auth_token(auth_client: AuthApiClient, default_user: User) -> str:
    response = auth_client.authorize(body=default_user.body_for_authorize)
    check_response_status(given=response.status_code, expected=HTTPStatus.OK)
    response_json = response.json()
    # TODO: Use model
    token = response_json.get('access_token')
    assert token, 'Access token should not be empty'
    return token


@pytest.fixture(scope='function')
def bff_client(auth_token: str, bff_host: str) -> BffApiClient:
    return BffApiClient(host=bff_host, token=auth_token)


@pytest.fixture(scope='function')
def root_node_ids_to_delete(bff_client: BffApiClient) -> list:
    node_ids = []
    yield node_ids
    undeleted = []
    for node_id in node_ids:
        resp = bff_client.delete_root_node(root_id=node_id)
        if resp.status_code != HTTPStatus.NO_CONTENT:
            undeleted.append(node_id)
    assert not undeleted, f'Nodes {undeleted} was not deleted'


# TODO: Create helpers for operations with entities (node deletion for example)
@pytest.fixture(scope='function')
def unit_type_ids_to_delete(bff_client: BffApiClient) -> list:
    type_ids = []
    yield type_ids
    undeleted = []
    for type_id in type_ids:
        # Get Marks
        marks_resp = bff_client.list_unit_marks()
        check_response_status(given=marks_resp.status_code, expected=HTTPStatus.OK)
        marks = UnitMarksListResponse(**marks_resp.json()).list
        # Delete Marks for that type
        for mark in marks:
            if mark.typeId == type_id:
                root_id = mark.unitId
                # Obtain root node tree
                units_resp = bff_client.list_unit_nodes_by_root_id(root_id=root_id)
                check_response_status(given=units_resp.status_code, expected=HTTPStatus.OK)
                nodes_dict = UnitNodesResponse(**units_resp.json()).nodes
                # Get root node children
                children_ids = nodes_dict[str(root_id)].childrenIds
                # Delete all child nodes
                for child_id in children_ids:
                    # Get tags for node
                    tags_resp = bff_client.list_tags(root_id=root_id, node_id=child_id)
                    check_response_status(given=tags_resp.status_code, expected=HTTPStatus.OK)
                    tags = TagsResponse(**tags_resp.json()).list
                    # Delete all tags
                    for tag in tags:
                        del_tag_resp = bff_client.delete_tag(root_id=root_id, node_id=child_id, tag_uuid=tag.uuid)
                    # Delete node
                    del_child_resp = bff_client.delete_unit_node(root_id=root_id, node_id=child_id)
                    check_response_status(given=del_child_resp.status_code, expected=HTTPStatus.NO_CONTENT)
                # Delete root unit node
                # TODO: Figure out why delete unit node request contains mark id https://app.clickup.com/t/85zrykdyd
                del_unit_root_resp = bff_client.delete_unit_node(root_id=mark.id, node_id=root_id)
                check_response_status(given=del_unit_root_resp.status_code, expected=HTTPStatus.NO_CONTENT)
                # Delete mark itself
                del_mark_resp = bff_client.delete_unit_mark(mark_id=mark.id)
                check_response_status(given=del_mark_resp.status_code, expected=HTTPStatus.NO_CONTENT)
        # Delete type
        resp = bff_client.delete_unit_type(type_id=type_id)
        if resp.status_code != HTTPStatus.NO_CONTENT:
            undeleted.append(type_id)
    assert not undeleted, f'Nodes {undeleted} was not deleted'
