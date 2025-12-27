import numpy as np
from helpers import load_text


def solve(fp):
    txt = load_text(fp).strip().split("\n")
    txt_nums = txt[:-1]
    txt_ops = txt[-1]

    nums = np.int64(
        list(
            map(
                lambda l: list(map(int, filter(lambda s: s != "", l.split(" ")))),
                txt_nums,
            )
        )
    )

    ops = list(filter(lambda s: s != "", txt_ops.split(" ")))

    return sum(
        np.prod(row) if ops[i] == "*" else np.sum(row)
        for i, row in enumerate(nums.transpose())
    )


def main():
    assert solve("p06_example.txt") == 4277556
    assert solve("p06_data.txt") == 6299564383938


main()
