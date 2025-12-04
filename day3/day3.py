from qwlist import Lazy
from utils.file import read_lines


def find_largest_from_n_batteries(string: str, n: int) -> int:
    ret = 0
    nums = [int(c) for c in string]
    start_index = 0
    last_available_index = len(nums) - n + 1
    slice_ = nums[start_index:last_available_index]
    for _ in range(n):
        ret *= 10
        m = max(slice_)
        ret += int(m)
        mi = slice_.index(m)
        start_index = mi + 1
        slice_ = slice_[start_index:]
        if last_available_index < len(nums):
            slice_.append(nums[last_available_index])
        last_available_index += 1
    return ret


def sol_a() -> int:
    res = (
        Lazy(read_lines('input.txt'))
        .map(lambda s: find_largest_from_n_batteries(s, 2))
        .sum()
    )
    return res


def sol_b() -> int:
    res = (
        Lazy(read_lines('input.txt'))
        .map(lambda s: find_largest_from_n_batteries(s, 12))
        .sum()
    )
    return res


def main():
    print(f'Solution a: {sol_a()}')
    print(f'Solution b: {sol_b()}')


if __name__ == '__main__':
    main()