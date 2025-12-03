import textwrap
from typing import Tuple, Dict
from qwlist import Lazy, QList
from utils.file import read_lines


def split(s: str) -> Tuple[str, str]:
    middle = len(s) // 2 + len(s) % 2
    return s[:middle], s[middle:]


def make_splits(s: str) -> QList[QList[str]]:
    ret = QList()
    for i in range(1, len(s)):
        splits = QList(textwrap.wrap(s, i))
        ret.append(splits)
    return ret


def occurred_at_least_twice(count: Dict[str, int]) -> bool:
    return QList(count.values()).all(lambda v: v >= 2)


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
    res = (
        Lazy(read_lines('input.txt'))
        .flatmap(lambda s: s.split(','))
        .filter(lambda s: len(s) > 0)
        .map(lambda s: s.split('-'))
        .map(lambda pair: (int(pair[0]), int(pair[1])))
        .flatmap(lambda pair: Lazy(str(i) for i in range(pair[0], pair[1] + 1)))
        .map(make_splits)
        .map(lambda sets: sets.filter(lambda nums: len(set(nums)) == 1).first())
        .filter(lambda x: x is not None)
        .map(''.join)
        .map(int)
        .sum()
    )
    return res


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()