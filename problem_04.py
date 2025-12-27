import numpy as np
from helpers import load_text


def load_map(fp):
    lines = load_text(fp).replace(".", "0").replace("@", "1").strip().split("\n")
    return np.int64([list(map(int, l)) for l in lines])


def pad(mat: np.ndarray):
    res = np.zeros((mat.shape[0] + 2, mat.shape[1] + 2), np.int64)
    res[1:-1, 1:-1] = mat
    return res


def unpad(mat: np.ndarray):
    return mat[1 : mat.shape[0] - 1, 1 : mat.shape[1] - 1]


def solve(fp):
    return solve_once(load_map(fp))[0]


def solve_once(mat):
    mat_pad = pad(mat)

    adj_count = np.zeros(mat_pad.shape, np.int64)

    for ir in range(1, mat_pad.shape[0] - 1):
        for ic in range(1, mat_pad.shape[1] - 1):
            mat_local = mat_pad[
                ir - 1 : ir + 2,
                ic - 1 : ic + 2,
            ]
            if mat_local[1, 1] == 1:
                adj_count[ir, ic] = np.sum(mat_local * mat_pad[ir, ic]) - 1
            else:
                adj_count[ir, ic] = 0

    adj_count = unpad(adj_count)

    removable = adj_count < 4

    mat_out = mat.copy()
    mat_out[removable] = 0
    total_removed = np.sum(removable * (mat != 0))
    return total_removed, mat_out


def solve_iter(fp):
    mat = load_map(fp)

    rem_sum = 0
    removed = -1

    while removed != 0:
        removed, mat = solve_once(mat)
        rem_sum += removed

    return rem_sum


def main():
    assert solve("p04_example.txt") == 13
    assert solve("p04_data.txt") == 1397

    assert solve_iter("p04_example.txt") == 43
    assert solve_iter("p04_data.txt") == 8758


main()
