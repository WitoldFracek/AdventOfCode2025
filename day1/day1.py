from qwlist import Lazy
from utils.file import read_lines
from utils.result import Result, Ok, Err
from typing import Tuple, Callable


def add_bounded(x: int, y: int, lower_bound: int, upper_bound: int) -> Result[int, str]:
    if lower_bound > upper_bound:
        return Err("Lower bound cannot be greater than upper bound")
    if y == 0:
        return Ok(x)
    mv = 0 - lower_bound
    diff = upper_bound - lower_bound
    x_mv = x + mv
    res_mv = (x_mv + y) % (diff + 1)
    res = res_mv - mv
    return Ok(res)


def add_and_count_zeros(acc: Tuple[int, int], fn: Callable[[int], int]) -> Tuple[int, int]:
    x, zeros = acc
    res = fn(x)
    if res == 0:
        zeros += 1
    return res, zeros

def add_and_count_zero_crossings(
        acc: Tuple[int, int],
        triplet: Tuple[str, int, Callable[[int, int], int]]
) -> Tuple[int, int]:
    x, crossings = acc
    direction, y, fn = triplet
    if y > 99:
        crossings += y // 100
    res = fn(x, y)
    if res == 0:
        return res, crossings
    if direction == 'R' and res < x:
        crossings += 1
    elif res > x:
        crossings += 1
    return res, crossings


def sol_a() -> int:
    add = lambda x, y: add_bounded(x, y, 0, 99).unwrap()
    sub = lambda x, y: add_bounded(x, -y, 0, 99).unwrap()
    return (
        Lazy(read_lines('input.txt'))
        .map(lambda s: (s[0], int(s[1:])))
        .map(lambda pair: lambda x: add(x, pair[1]) if pair[0] == 'R' else sub(x, pair[1]))
        .fold(add_and_count_zeros,(50, 0))[1]
    )


def sol_b() -> int:
    add = lambda x, y: add_bounded(x, y, 0, 99).unwrap()
    sub = lambda x, y: add_bounded(x, -y, 0, 99).unwrap()
    return (
        Lazy(read_lines('input.txt'))
        .map(lambda s: (s[0], int(s[1:])))
        .map(lambda pair: (pair[0], pair[1], add if pair[0] == 'R' else sub))
        .fold(add_and_count_zero_crossings, (50, 0))[1]
    )


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')  # Too high: 7404


if __name__ == '__main__':
    main()