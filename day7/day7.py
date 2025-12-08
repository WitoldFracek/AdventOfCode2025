from qwlist import Lazy, QList
from utils.file import read_lines
from utils.option import Option, Some, None_
from utils.result import Result, Ok, Err
import utils.result as result

type Grid = QList[QList[str]]
type NumGrid = QList[QList[int]]


def propagate_stream(grid: Grid) -> Grid:
    s_pos = grid[0].index('S')
    grid[1][s_pos] = '|'
    for i, row in grid.enumerate().skip(1):
        for j, col in row.enumerate():
            if col == '^':
                row[j - 1] = '|'
                row[j + 1] = '|'
            if col == '.' and grid[i - 1][j] == '|':
                row[j] = '|'
    return grid


def propagate_quantum_stream(grid: Grid) -> NumGrid:
    s_pos = grid[0].index('S')
    grid[1][s_pos] = '|'
    grid = propagate_stream(grid)
    num_grid = grid.map(lambda row: row.map(lambda x: 0).collect()).collect()
    num_grid[1][s_pos] = 1

    for i, row in grid.enumerate().skip(1):
        for j, col in row.enumerate():
            if col == '^':
                if j-1 >= 0:
                    num_grid[i][j-1] += num_grid[i-1][j]
                if j+1 < row.len():
                    num_grid[i][j+1] += num_grid[i-1][j]
            if col == '|':
                num_grid[i][j] += num_grid[i-1][j]
    return num_grid



def sol_a() -> int:
    grid: QList[QList[str]] = Lazy(read_lines('input.txt')).map(lambda line: QList(line)).collect()
    grid = propagate_stream(grid)
    counter = 0
    for row1, row2 in grid.window(2):
        for c1, c2 in row1.zip(row2):
            if c1 == '|' and c2 == '^':
                counter += 1
    return counter


def sol_b() -> int:
    grid: QList[QList[str]] = Lazy(read_lines('input.txt')).map(lambda line: QList(line)).collect()
    num_grid = propagate_quantum_stream(grid)
    res = num_grid[-1].sum()
    return res


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()