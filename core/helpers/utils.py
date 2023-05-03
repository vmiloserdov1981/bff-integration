import requests


def check_response_status(given: int, expected: int) -> None:
    assert given == expected, f'Given status code {given} is not equal to expected one {expected}'
