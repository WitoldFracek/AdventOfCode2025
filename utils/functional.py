from typing import Tuple


def first[T, K](pair: Tuple[T, K]) -> T:
    return pair[0]


def second[T, K](pair: Tuple[T, K]) -> K:
    return pair[1]