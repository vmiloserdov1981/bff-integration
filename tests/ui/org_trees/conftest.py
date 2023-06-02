import pytest

from core.helpers.utils import uniq_timestamp
from core.models.unit_type import UnitType


@pytest.fixture(scope='function')
def root_org_node_name() -> str:
    return f'org_root_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def second_root_org_node_name() -> str:
    return f'org_root_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def child_org_node_name() -> str:
    return f'org_child_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def leaf_org_node_name() -> str:
    return f'org_leaf_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def unit_type_name() -> str:
    return f'unit_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def mark_name() -> str:
    return f'mark_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def child_unit_node_name() -> str:
    return f'child_node_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def subchild_unit_node_name() -> str:
    return f'subchild_node_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def branch_name() -> str:
    return f'Branch_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def unit_name() -> str:
    return f'unit_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def unit_type_scaffold(unit_type_name: str) -> UnitType:
    return UnitType(name=unit_type_name)


@pytest.fixture(scope='function')
def unit_mark_name(unit_type_name: str) -> str:
    return f'brand_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def root_unit_node_name(unit_mark_name: str) -> str:
    return f'gener_{uniq_timestamp()}'
