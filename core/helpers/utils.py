import ast
import os
import time
from pathlib import Path
from typing import Union

M = int(1e6)


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def env_path() -> Path:
    return get_project_root().joinpath('.env')


def check_response_status(given: int, expected: int) -> None:
    assert given == expected, f'Given status code {given} is not equal to expected one {expected}'


def timestamp() -> int:
    return time.time_ns() // M


def uniq_timestamp() -> int:
    ts = timestamp()
    time.sleep(1.0 / 1000)
    return ts


def get_env_var(name: str) -> Union[str, None]:
    variable = os.environ.get(name)
    return variable


def get_and_check_env_var(name: str) -> str:
    variable = get_env_var(name=name)
    assert variable is not None, f'Variable {name} is not provided'
    return variable


def get_env_variable_as_dict(name: str) -> dict:
    var = get_env_var(name)
    if var:
        dict_var = ast.literal_eval(var)
        return dict_var
    return {}
