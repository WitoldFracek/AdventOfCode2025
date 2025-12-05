from qwlist import Lazy, QList
from utils.file import read_lines
from typing import List, Tuple


def convolve(matrix: List[List[int]], kernel: List[List[int]]) -> List[List[int]]:
    m_rows = len(matrix)
    m_cols = len(matrix[0]) if m_rows > 0 else 0
    k_rows = len(kernel)
    k_cols = len(kernel[0]) if k_rows > 0 else 0
    pad_height = k_rows // 2
    pad_width = k_cols // 2

    padded_matrix = [[0] * (m_cols + 2 * pad_width) for _ in range(pad_height)]
    for row in matrix:
        padded_matrix.append([0] * pad_width + row + [0] * pad_width)
    padded_matrix.extend([[0] * (m_cols + 2 * pad_width) for _ in range(pad_height)])

    output = [[0 for _ in range(m_cols)] for _ in range(m_rows)]
    for i in range(m_rows):
        for j in range(m_cols):
            conv_sum = 0
            for ki in range(k_rows):
                for kj in range(k_cols):
                    conv_sum += (padded_matrix[i + ki][j + kj] * kernel[ki][kj])
            output[i][j] = conv_sum
    return output


def flag_rolls_for_removal(matrix: List[List[int]], kernel: List[List[int]]) -> List[List[bool]]:
    convolved = convolve(matrix, kernel)
    m_rows = len(matrix)
    m_cols = len(matrix[0]) if m_rows > 0 else 0
    removal_flags = [[False for _ in range(m_cols)] for _ in range(m_rows)]
    for i in range(m_rows):
        for j in range(m_cols):
            if 100 <= convolved[i][j] < 104:
                removal_flags[i][j] = True
    return removal_flags


def first_true_flag(matrix: List[List[bool]]) -> Tuple[int, int] | None:
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val:
                return i, j
    return None


def sol_a() -> int:
    matrix = (
        Lazy(read_lines('input.txt'))
        .map(lambda row: Lazy(row).map(lambda c: 1 if c == '@' else 0).collect())
        .collect()
    )
    matrix = QList(convolve(
        matrix=matrix,
        kernel=[
            [1, 1, 1],
            [1, 100, 1],
            [1, 1, 1]
        ]
    ))
    res = (
        matrix
        .flatmap(lambda row: QList(row).map(lambda v: 100 <= v < 104).collect())
        .sum()
    )
    return res


def sol_b() -> int:
    matrix = (
        Lazy(read_lines('input.txt'))
        .map(lambda row: Lazy(row).map(lambda c: 1 if c == '@' else 0).collect())
        .collect()
    )
    flags = flag_rolls_for_removal(
        matrix=matrix,
        kernel=[
            [1, 1, 1],
            [1, 100, 1],
            [1, 1, 1]
        ]
    )
    coords = first_true_flag(flags)
    counter = 0
    while coords:
        x, y = coords
        matrix[x][y] = 0
        flags = flag_rolls_for_removal(
            matrix=matrix,
            kernel=[
                [1, 1, 1],
                [1, 100, 1],
                [1, 1, 1]
            ]
        )
        coords = first_true_flag(flags)
        counter += 1
    return counter


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()