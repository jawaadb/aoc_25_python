import numpy as np
from helpers import load_text


def load_map(fp):
    lines = load_text(fp).replace(".", "0").replace("@", "1").strip().split("\n")
    return np.int64([list(map(int, l)) for l in lines])


def pad(mat: np.ndarray):
    res = np.zeros((mat.shape[0] + 2, mat.shape[1] + 2), np.int64)
    res[1:-1, 1:-1] = mat
    return res


def convolve2d(mA: np.ndarray, mB: np.ndarray):
    res = np.int64(
        [
            np.sum(
                [
                    np.convolve((mA[ir, :]), mB[jr, :], "same")
                    for jr in range(mB.shape[0])
                ],
                axis=0,
            )
            for ir in range(1, mA.shape[0] - 1)
        ]
    )[:, 1:-1]

    return res


def solve(fp):
    mat_pad = pad(mat := load_map(fp))

    res = np.zeros(mat_pad.shape, np.int64)

    for ir in range(1, mat_pad.shape[0] - 1):
        for ic in range(1, mat_pad.shape[1] - 1):
            mat_local = mat_pad[
                ir - 1 : ir + 2,
                ic - 1 : ic + 2,
            ]
            if mat_local[1, 1] == 1:
                res[ir, ic] = np.sum(mat_local * mat_pad[ir, ic]) - 1
            else:
                res[ir, ic] = 0

    res = res[1 : res.shape[0] - 1, 1 : res.shape[1] - 1]

    return np.sum((res < 4) * (mat != 0))


def main():
    assert solve("p04_example.txt") == 13
    assert solve("p04_data.txt") == 1397


main()
