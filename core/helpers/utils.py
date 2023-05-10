import time


M = int(1e6)


def check_response_status(given: int, expected: int) -> None:
    assert given == expected, f'Given status code {given} is not equal to expected one {expected}'


def timestamp() -> int:
    return time.time_ns() // M


def uniq_timestamp() -> int:
    ts = timestamp()
    time.sleep(1.0 / 1000)
    return ts
