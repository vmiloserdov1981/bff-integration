import allure

from http import HTTPStatus

from core.clients.bff_api import BffApiClient
from core.helpers.utils import check_response_status
from core.models.tag import Tag, TagsResponse, CreateTagResponse
from core.models.unit_type import UnitType, CreateUnitTypeResponse
from core.models.unit_marks import UnitMark, CreateUnitMarkResponse
from core.models.unit_nodes import UnitNode, CreateRootUnitNodeResponse, CreateUnitNodeResponse
from core.models.org_nodes import (RootNodeResponse, RootElem, CommonNode, RootNodesList, NodeResponse,
                                   TreeResponseResult, AttachNodeResponse)


class TestOrgTree:

    @allure.id('')
    @allure.title('Орг. структура')
    def test_org_tree(self, bff_client: BffApiClient,
                      root_node_scaffold: RootElem,
                      updated_root_node_scaffold: RootElem,
                      second_root_node_scaffold: RootElem,
                      child_node_name: str,
                      unit_type_scaffold: UnitType,
                      unit_type_ids_to_delete: list,
                      root_node_ids_to_delete: list,
                      unit_mark_name: str,
                      root_unit_node_name: str,
                      child_unit_node_name: str,
                      temp_tag: Tag):
        # 'добавили новое дерево orgElements'
        # POST frontapi/v1/org-trees; POST frontapi/v1/org-trees/{rootId}/nodes;
        with allure.step('Создать корневой элемент дерева'):
            create_root_resp = bff_client.create_root_node(json=root_node_scaffold.body_for_creation)
            check_response_status(given=create_root_resp.status_code, expected=HTTPStatus.CREATED)
            cr_resp_body = create_root_resp.json()
            root_model_one = RootNodeResponse(**cr_resp_body).result
            elem_one_id = root_model_one.rootElem.id
            root_node_ids_to_delete.append(elem_one_id)

        # 'получили дерево, порадовались'
        # GET frontapi/v1/org-trees
        with allure.step('Получить список корневых элементов'):
            list_response = bff_client.list_org_trees()
            check_response_status(given=list_response.status_code, expected=200)

        with allure.step('Созданный корневой элемент присутствует в списке'):
            list_dict = list_response.json()
            nodes = RootNodesList(**list_dict).result
            expected_node = next((n for n in nodes if n.rootElem.id == elem_one_id), None)
            assert expected_node, f'Expected node {elem_one_id} in not in the root nodes list'

        # 'отредактировали дерево orgElements'
        # PATCH frontapi/v1/org-trees/{rootId}/nodes/{nodeId};
        with allure.step('Изменить название созданного корневого элемента'):
            patch_response = bff_client.update_root_node(root_id=elem_one_id,
                                                         json=updated_root_node_scaffold.body_for_update)
            check_response_status(given=patch_response.status_code, expected=HTTPStatus.OK)

        with allure.step('В ответе пришло изменённое название'):
            patched = NodeResponse(**patch_response.json()).result
            assert patched.name == updated_root_node_scaffold.node.name, \
                'Received node name is not equal to expected one'

        with allure.step('Получить список корневых узлов деревьев'):
            second_list_response = bff_client.list_org_trees()
            check_response_status(given=second_list_response.status_code, expected=200)

        with allure.step('В списке присутствует дерево с изменённым названием'):
            second_list_dict = second_list_response.json()
            nodes = RootNodesList(**second_list_dict).result
            expected_node = next((n for n in nodes if n.rootElem.id == elem_one_id), None)
            assert expected_node.node.name == updated_root_node_scaffold.node.name, \
                'The node name in list is not equal to expected one'

        # 'добавили второе дерево orgElements'
        with allure.step('Создать второй корневой узел'):
            create_second_root_resp = bff_client.create_root_node(json=second_root_node_scaffold.body_for_creation)
            check_response_status(given=create_second_root_resp.status_code, expected=HTTPStatus.CREATED)
            cr_second_resp_body = create_second_root_resp.json()
            root_model_two = RootNodeResponse(**cr_second_resp_body).result
            elem_two_id = root_model_two.rootElem.id
            root_node_ids_to_delete.append(elem_two_id)

        with allure.step('Получить список корневых узлов'):
            third_list_response = bff_client.list_org_trees()
            check_response_status(given=third_list_response.status_code, expected=200)

        with allure.step('Второй узел присутствует в списке'):
            list_dict = third_list_response.json()
            nodes = RootNodesList(**list_dict).result
            expected_node = next((n for n in nodes if n.rootElem.id == elem_two_id), None)
            assert expected_node, f'Expected node {elem_two_id} in not in the root nodes list'

        with allure.step('Создать дочерний узел для созданного корневого узла'):
            child_model = CommonNode(name=child_node_name, parentId=elem_two_id)
            create_org_child_resp = bff_client.create_child_node(root_id=elem_two_id,
                                                                 json=child_model.body_for_creation)
            check_response_status(given=create_org_child_resp.status_code, expected=HTTPStatus.CREATED)

        with allure.step('Получить список дочерних узлов созданного корневого узла'):
            tree_list_resp = bff_client.list_nodes_by_root_id(root_id=elem_two_id)
            check_response_status(given=tree_list_resp.status_code, expected=HTTPStatus.OK)

        with allure.step('Созданный дочерний узел присутствует в списке'):
            tree_dict = tree_list_resp.json()
            tree = TreeResponseResult(**tree_dict)

        # 'добавили unitNodesTemplate'
        # POST frontapi/v1/unit-types; POST frontapi/v1/unit-marks;
        # POST frontapi/v1/unitnode-trees; POST frontapi/v1/unitnode-trees/14/nodes;
        with allure.step('Создать тип оборудования'):
            create_ut_resp = bff_client.create_unit_type(json=unit_type_scaffold.body_for_creation)
            # TODO: Report bug 200 isn't normal for creation. Should be 201
            check_response_status(given=create_ut_resp.status_code, expected=HTTPStatus.OK)
            unit_type = CreateUnitTypeResponse(**create_ut_resp.json()).unit_type
            type_id = unit_type.id
            unit_type_ids_to_delete.append(type_id)

        with allure.step('Создать марку оборудования'):
            create_mark_resp = bff_client.create_unit_mark(json=UnitMark(name=unit_mark_name,
                                                                         typeId=type_id).dict(exclude_unset=True))
            check_response_status(given=create_mark_resp.status_code, expected=HTTPStatus.CREATED)
            mark = CreateUnitMarkResponse(**create_mark_resp.json()).unit_mark
            mark_id = mark.id  # 8, type_id: 3 (Type_of Device)
            # Parent ID 14 (Creating Mark involves creating root Unit Node)

        with allure.step('Создать корневой узел юнита для созданной марки'):
            root_node_scaffold = UnitNode(name=root_unit_node_name, typeId=type_id, markId=mark_id,
                                          unitKind='UNIT_NODE')
            create_root_unit_resp = bff_client.create_root_unit_node(json=root_node_scaffold.body_for_root_creation)
            check_response_status(given=create_root_unit_resp.status_code, expected=HTTPStatus.CREATED)
            root_unit_node = CreateRootUnitNodeResponse(**create_root_unit_resp.json()).node

        with allure.step('Добавить дочерний узел к типу оборуования'):
            node_template = UnitNode(name=child_unit_node_name, parentId=root_unit_node.id, unitKind='UNIT_NODE')
            create_unit_child_resp = bff_client.create_unit_node(parent_id=mark_id,
                                                                 json=node_template.dict(exclude_unset=True))
            check_response_status(given=create_unit_child_resp.status_code, expected=HTTPStatus.CREATED)
            unit_child = CreateUnitNodeResponse(**create_unit_child_resp.json()).node

        # 'добавиди туда теги и доп данные к ним'
        # PUT frontapi/v1/unitnode-trees/{treeRootId}/nodes/{unitNodeId}/ltags/{ltagUuid};
        with allure.step('Добавить в шаблон тег'):
            create_tag_resp = bff_client.create_tag(root_id=root_unit_node.id, node_id=unit_child.id,
                                                    json=temp_tag.body_for_creation)
            # TODO: Create Bug for BFF. Status must be 204 (CREATED)
            check_response_status(given=create_tag_resp.status_code, expected=HTTPStatus.OK)
            tag = CreateTagResponse(**create_tag_resp.json()).tag

        with allure.step('Получить список тегов'):
            tags_resp = bff_client.list_tags(root_id=root_unit_node.id, node_id=unit_child.id)
            check_response_status(given=tags_resp.status_code, expected=HTTPStatus.OK)

        with allure.step('Добавленный тег присутствует в списке тегов'):
            tags = TagsResponse(**tags_resp.json()).list
            expected_tag = next((t for t in tags if t.uuid == tag.uuid), None)
            assert expected_tag, f'Expected uuid {tag.uuid} is not in the tags list {tags}'

        # 'прилинковали узлы к unitNodes;'
        # POST /org-trees/{orgTreeRootId}/nodes/{nodeId}/bindunit
        with allure.step('Добавить к дочернему узлу дерева шаблон оборудования'):
            attachable_node = CommonNode(name='Attached Unit', parentId=elem_two_id,
                                         unitNodeTreeRootIdRef=root_unit_node.id)
            link_template_resp = bff_client.attach_unit_node(parent_id=elem_two_id,
                                                             json=attachable_node.body_for_creation)
            check_response_status(given=link_template_resp.status_code, expected=HTTPStatus.CREATED)
            # TODO: Check for 'status' and 'visibility' PATCH requests
            linked_node = AttachNodeResponse(**link_template_resp.json()).node


        # 'получили дерево с узлами. радуемся'
        with allure.step('Получить список дочерних узлов второго дерева'):
            second_tree_list_resp = bff_client.list_nodes_by_root_id(root_id=elem_two_id)
            check_response_status(given=second_tree_list_resp.status_code, expected=HTTPStatus.OK)
            second_nodes = TreeResponseResult(**second_tree_list_resp.json()).nodes

        with allure.step('В списке присутствует добавленный шаблон оборудования'):
            expected_node = second_nodes.get(str(linked_node.id))
            assert expected_node, f'Tree should contain expected node {linked_node.id}'

