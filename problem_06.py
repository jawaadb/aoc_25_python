import numpy as np
from helpers import load_text


def solve2(fp):
    txt = list(filter(lambda line: len(line) != 0, load_text(fp).split("\n")))
    arr = np.array([list(l) for l in txt])[:, ::-1].transpose()
    arr = arr[~np.all(arr == " ", axis=1), :]

    problems: list[list[int], str] = []

    acc: list[int] = []
    is_last = False
    for l in ["".join(l) for l in arr]:
        l = l.strip()
        match l[-1]:
            case "*" | "+":
                num = int(l[:-1])
                is_last = True
            case _:
                num = int(l)

        acc += [num]
        if is_last:
            problems += [[acc, l[-1]]]
            acc = []
            is_last = False

    return sum(np.sum(p[0]) if p[-1] == "+" else np.prod(p[0]) for p in problems)


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

    assert solve2("p06_example.txt") == 3263827
    assert solve2("p06_data.txt") == 11950004808442


main()
