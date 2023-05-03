import pytest

from http import HTTPStatus

from core.clients.bff_api import BffApiClient
from core.models.org_nodes import CommonNode, RootElem
from core.models.tag import Tag, DeadZone, Thresholds, ThresholdItem, ParamRange, ParamItem
from core.models.unit_type import UnitType


@pytest.fixture(scope='function')
def root_node_name() -> str:
    return 'L1-at'


@pytest.fixture(scope='function')
def child_node_name() -> str:
    return 'L2-child'


@pytest.fixture(scope='function')
def root_node_updated_name(root_node_name: str) -> str:
    return f'{root_node_name} updated'


@pytest.fixture(scope='function')
def root_node_scaffold(root_node_name: str) -> RootElem:
    node = CommonNode(name=root_node_name)
    return RootElem(rootElem=node)


@pytest.fixture(scope='function')
def second_root_node_scaffold(root_node_name: str) -> RootElem:
    node = CommonNode(name=f'{root_node_name} the second')
    return RootElem(rootElem=node)


@pytest.fixture(scope='function')
def updated_root_node_scaffold(root_node_scaffold: RootElem, root_node_updated_name: RootElem) -> RootElem:
    node = CommonNode(name=root_node_updated_name)
    return RootElem(rootElem=node)


@pytest.fixture(scope='function')
def unit_type_name() -> str:
    # TODO: Add generator
    return 'ST-EE-PLiPP-360'


@pytest.fixture(scope='function')
def unit_type_scaffold(unit_type_name: str) -> UnitType:
    return UnitType(name=unit_type_name)


@pytest.fixture(scope='function')
def unit_mark_name(unit_type_name: str) -> str:
    # TODO: Add generator
    return f'{unit_type_name}::BFG-3030'


@pytest.fixture(scope='function')
def root_unit_node_name(unit_mark_name: str) -> str:
    # TODO: Add generator
    return f'{unit_mark_name}::RCH'


@pytest.fixture(scope='function')
def child_unit_node_name(root_unit_node_name: str) -> str:
    # TODO: Add generator
    return f'{root_unit_node_name}::FCH'


@pytest.fixture(scope='function')
def temp_tag() -> Tag:
    return Tag(
        title='Test Temp Tag',
        physicalQuantity='TEMPERATURE',
        physicalQuantityUnit='C',
        markedAsObservable=True,
        deadZone=DeadZone(type='RELATIVE', value=0),
        thresholds=Thresholds(
            upper=[
                ThresholdItem(value=0, severity='urgent', isActive=False),
                ThresholdItem(value=0, severity='high', isActive=False),
                ThresholdItem(value=37, severity='low', isActive=True)
            ],
            lower=[
                ThresholdItem(value=35, severity='urgent', isActive=True),
                ThresholdItem(value=0, severity='high', isActive=False),
                ThresholdItem(value=0, severity='low', isActive=False)
            ]
        ),
        operatingRange=ParamRange(
            upper=ParamItem(value=42, isActive=True),
            lower=ParamItem(value=30, isActive=True)
        ),
        displayRange=ParamRange(
            upper=ParamItem(value=44, isActive=True),
            lower=ParamItem(value=28, isActive=True)
        ),
        unitId=0,
        namedValues=[]
    )

