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
    lines = QList(read_lines('input.txt', do_strip=False)).map(lambda s: s.replace('\n', ''))
    nums_and_ops = Lazy(zip_longest(*lines, fillvalue=' '))
    total = 0
    acc = []
    acc_op = None
    for row in nums_and_ops:
        *digits, op = row
        digits = [d.strip() for d in digits]
        num = ''.join(digits)
        if op != ' ':
            acc_op = op
        if not num:
            total += sum(acc) if acc_op == '+' else mul(*acc)
            acc_op = None
            acc = []
        else:
            acc.append(int(num))
    if acc:
        total += sum(acc) if acc_op == '+' else mul(*acc)
    return total


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()
