from .enemy import *

__all__ = ["level"]


def level():
    yield from EnemyBlockAI().spawn(4, 8)

    yield
    yield from EnemyBlockAI().spawn(5, 12)

    yield
    yield from SnakeAI().spawn(64)

    i = 6
    while True:
        i += 1
        yield
        yield from SnakeAI().spawn(2 ** i)
        yield from EnemyBlockAI().spawn(8, 16)
