from qwlist import Lazy
from utils.file import read_lines
from typing import Tuple


def split(s: str) -> Tuple[str, str]:
    middle = len(s) // 2 + len(s) % 2
    return s[:middle], s[middle:]


def sol_a() -> int:
    res = (
        Lazy(read_lines('input.txt'))
        .flatmap(lambda s: s.split(','))
        .filter(lambda s: len(s) > 0)
        .map(lambda s: s.split('-'))
        .map(lambda pair: (int(pair[0]), int(pair[1])))
        .map(lambda pair: Lazy(str(i) for i in range(pair[0], pair[1] + 1)))
        .flatmap(lambda xs: xs.map(split)
             .filter(lambda pair: pair[0] == pair[1])
             .map(''.join)
             .map(int)
        )
        .filter(lambda num: num is not None)
        .sum()
    )
    return res


def sol_b() -> int:
    return -1


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()