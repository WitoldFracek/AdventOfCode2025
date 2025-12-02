from typing import Tuple


def fst[T, K](pair: Tuple[T, K]) -> T:
    return pair[0]


def snd[T, K](pair: Tuple[T, K]) -> K:
    return pair[1]