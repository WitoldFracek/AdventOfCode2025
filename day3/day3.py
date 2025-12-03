from qwlist import Lazy, QList
from utils.file import read_lines
from utils.option import Option, Some, None_
from utils.result import Result, Ok, Err
import utils.result as result


def possible_jolts(s: str) -> Lazy[int]:
    return (
        QList(s[:-1]).enumerate().flatmap(lambda idx_char:
            QList(s)
            .skip(idx_char[0] + 1)
            .map(lambda c: (idx_char[1], c))
            .map(''.join)
            .map(int)
        )
    )


def find_largest_from_n_batteries(s: str, n: int) -> int:
    digits = QList(s).map(int).collect()
    maxes = QList()
    for _ in range(n):
        current_max = max(digits)
        i = digits.index(current_max)
        maxes.append((i, current_max))
        digits[i] = 0
    return int(''.join(
        maxes
        .sorted(key=lambda pair: pair[0])
        .map(lambda pair: str(pair[1]))
    ))



def sol_a() -> int:
    res = (
        Lazy(read_lines('input.txt'))
        .map(possible_jolts)
        .map(lambda ls: ls.max())
        .sum()
    )
    return res


def sol_b() -> int:
    res = (
        Lazy(read_lines('test.txt'))
        .map(lambda x: find_largest_from_n_batteries(x, 12))

    )
    res.foreach(print)
    return res


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()