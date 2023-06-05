import pytest

from core.helpers.utils import uniq_timestamp
from core.models.unit_type import UnitType


@pytest.fixture(scope='function')
def rules_name() -> str:
    return f'Rules_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def unit_type_scaffold(unit_type_name: str) -> UnitType:
    return UnitType(name=unit_type_name)


@pytest.fixture(scope='function')
def description() -> str:
    return f'Description_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def description_edit() -> str:
    return f'Description_edit{uniq_timestamp()}'
