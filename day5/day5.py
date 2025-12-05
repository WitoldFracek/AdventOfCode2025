from qwlist import Lazy, QList
from utils.file import read_lines
from typing import Iterable, Tuple


class Range:
    def __init__(self, min_: int, max_: int):
        self.min_ = min_
        self.max_ = max_

    def __contains__(self, item: int) -> bool:
        return self.min_ <= item <= self.max_

    def __repr__(self) -> str:
        return f'Range({self.min_}, {self.max_})'

    def __len__(self) -> int:
        return self.max_ - self.min_ + 1


class ComplexRange:
    def __init__(self, ranges: Iterable[Tuple[int, int]]):
        ranges = QList(sorted(ranges, key=lambda r: r[0]))
        self.ranges = ComplexRange.reduce_ranges(ranges).map(lambda r: Range(r[0], r[1]))

    @staticmethod
    def reduce_ranges(ranges: QList[Tuple[int, int]]) -> QList[Tuple[int, int]]:
        if ranges.len() < 2:
            return ranges
        reduced_ranges = QList()
        lower = ranges[0]
        for upper_range in ranges.skip(1):
            reduced = ComplexRange.reduce_range(lower, upper_range)
            if reduced.len() == 1:
                lower = reduced[0]
            else:
                lower = reduced[1]
                reduced_ranges.append(reduced[0])
        if lower:
            reduced_ranges.append(lower)
        return reduced_ranges

    @staticmethod
    def reduce_range(r1: Tuple[int, int], r2: Tuple[int, int]) -> QList[Tuple[int, int]]:
        if r1[1] < r2[0]:
            return QList([r1, r2])
        return QList([(r1[0], max(r1[1], r2[1]))])

    def __contains__(self, item: int) -> bool:
        return self.ranges.any(lambda r: item in r)

    def __len__(self) -> int:
        return self.ranges.map(len).sum()

    def __repr__(self) -> str:
        return f'ComplexRange({self.ranges})'


def sol_a() -> int:
    ranges, numbers = (
        Lazy(read_lines('input.txt'))
        .split_when(lambda line: line == '')
    )
    ranges: QList[Range] = (
        ranges
        .filter(lambda line: line != '')
        .map(lambda line: line.split('-'))
        .map(lambda parts: Range(int(parts[0]), int(parts[1])))
        .collect()
    )
    res = (
        numbers
        .filter(lambda line: line != '')
        .map(int)
        .filter(lambda num: ranges.any(lambda r: num in r))
        .collect()
    ).len()
    return res


def sol_b() -> int:
    res = (
        Lazy(read_lines('input.txt'))
        .take_while(lambda line: line != '')
        .map(lambda line: line.split('-'))
        .map(lambda parts: (int(parts[0]), int(parts[1])))
    )
    cr = ComplexRange(res)
    return len(cr)


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()