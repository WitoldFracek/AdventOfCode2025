from qwlist import Lazy, QList
from utils.file import read_lines
from itertools import zip_longest


def mul(*args) -> int:
    fst = args[0]
    return QList(args).skip(1).fold(lambda acc, x: acc * x, fst)


def sol_a() -> int:
    file_name = 'input.txt'
    first_line = Lazy(read_lines(file_name)).first()
    count = Lazy(first_line.split(' ')).filter(lambda s: s != '').collect().len()
    res = (
        Lazy(read_lines(file_name))
        .flatmap(lambda line:
            Lazy(line.split(' '))
            .filter(lambda s: s != '')
        )
        .enumerate()
        .group_by(lambda pair: pair[0] % count)
        .map(lambda group:
            group
            .map(lambda x: x[1])
            .collect()
        )
        .map(lambda line: (line[:-1].map(int), line[-1]))
        .map(lambda pair: sum(pair[0]) if pair[1] == '+' else mul(*pair[0]))
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
