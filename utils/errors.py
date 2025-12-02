from typing import Never

class UnrecoverableError(Exception):
    pass


def panic(msg: str) -> Never:
    """
    Raises an UnrecoverableError with the given message.

    Args:
        msg (str): message to be displayed in the error.
    """
    raise UnrecoverableError(msg)