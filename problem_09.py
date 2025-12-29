import numpy as np
from helpers import load_text


def load(fp):
    return np.int64(
        [list(map(int, l.split(","))) for l in load_text(fp).strip().split("\n")]
    )


def solve(fp):
    pts = load(fp)
    num_pts = pts.shape[0]

    areas = np.int64(
        [
            np.prod(
                np.abs(pts - np.repeat(pt.reshape((1, -1)), num_pts, axis=0))
                + np.repeat([[1, 1]], num_pts, axis=0),
                axis=1,
            )
            for pt in pts
        ]
    )
    return areas.max()


def main():
    assert solve("p09_example.txt") == 50
    assert solve("p09_data.txt") == 4758121828


main()
