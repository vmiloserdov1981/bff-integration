import pytest

from core.helpers.utils import uniq_timestamp


@pytest.fixture(scope='function')
def rules_name() -> str:
    return f'Rules_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def description() -> str:
    return f'Description_{uniq_timestamp()}'


@pytest.fixture(scope='function')
def description_edit() -> str:
    return f'Description_edit{uniq_timestamp()}'
