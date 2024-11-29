from typing import NoReturn


def todo(what: str = '') -> NoReturn:
    raise NotImplementedError(f'Not Implemented, TODO: {what}')