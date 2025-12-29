import numpy as np
from numpy.linalg import norm
from helpers import load_text


def load(fp) -> np.ndarray:
    return np.int64(
        [list(map(int, l.split(","))) for l in load_text(fp).strip().split("\n")]
    )


def calc_dist_mat(pts: np.ndarray):
    dist_mat = np.float64(
        [
            norm(pts - np.repeat(pa.reshape((1, -1)), pts.shape[0], axis=0), axis=1)
            for pa in pts
        ]
    )
    assert np.all(dist_mat == dist_mat.transpose())
    return dist_mat


def find_shortest_not_connected(dist_mat: np.ndarray, conn_mat: np.ndarray):
    assert dist_mat.shape[0] == dist_mat.shape[1]
    assert conn_mat.shape == dist_mat.shape

    iyy, ixx = np.indices(dist_mat.shape)

    min_val = dist_mat[(np.eye(dist_mat.shape[0]) != 1) & (~conn_mat)].min()

    found = dist_mat == min_val
    coords = np.vstack([iyy[found], ixx[found]]).transpose()
    return coords


def connect_shortest(
    dist_mat: np.ndarray, conn_mat: np.ndarray, conn_mat_distilled: np.ndarray
):
    coords = find_shortest_not_connected(dist_mat, conn_mat)
    assert np.all(coords[0, :] == coords[1, ::-1])
    for pt in coords:
        conn_mat[*pt] = True
        conn_mat_distilled[*pt] = True

    for i in coords[0, :]:
        conn_mat_distilled[i, i] = True

    distill(conn_mat_distilled)

    return coords[0, :]


def is_distilled(conn_mat: np.ndarray) -> bool:
    return np.all(np.sum(conn_mat, axis=0) == 1)


def distill(conn_mat: np.ndarray):
    idx_dups = np.where(np.sum(conn_mat, axis=0) > 1)[0]
    for ic in idx_dups:
        idx_rows = np.where(conn_mat[:, ic])[0]
        row_union = np.any(conn_mat[idx_rows, :], axis=0)
        conn_mat[idx_rows[0], :] = row_union
        conn_mat[idx_rows[1:], :] = False

    assert is_distilled(conn_mat)


def connected_groups(conn_mat: np.ndarray):
    assert is_distilled(conn_mat)

    indices = np.arange(conn_mat.shape[1])
    return sorted(
        filter(lambda g: np.size(g) != 0, (indices[row] for row in conn_mat)),
        key=np.size,
        reverse=True,
    )


def solve(fp, num_of_connections, num_to_take):
    arr = load(fp)

    dist_mat = calc_dist_mat(arr)
    conn_mat = np.eye(arr.shape[0], dtype=np.bool)
    conn_mat_distilled = conn_mat.copy()

    for _ in range(num_of_connections):
        connect_shortest(dist_mat, conn_mat, conn_mat_distilled)

    assert is_distilled(conn_mat_distilled)
    groups = connected_groups(conn_mat_distilled)
    return np.prod(list(map(np.size, groups[:num_to_take])))


def solve2(fp) -> int:
    arr = load(fp)

    dist_mat = calc_dist_mat(arr)
    conn_mat = np.eye(arr.shape[0], dtype=np.bool)
    conn_mat_distilled = conn_mat.copy()

    while True:
        coords = connect_shortest(dist_mat, conn_mat, conn_mat_distilled)

        num_groups = np.sum(np.any(conn_mat_distilled, axis=1))
        print(
            f"num_groups: {num_groups:>3d} / {conn_mat_distilled.shape[0]}",
            end="\r",
            flush=True,
        )
        if num_groups == 1:
            print()
            break

    return np.prod(arr[coords, 0])


def main():
    assert solve("p08_example.txt", 10, 3) == 40
    assert solve("p08_data.txt", 1000, 3) == 123234

    assert solve2("p08_example.txt") == 25272
    assert solve2("p08_data.txt") == 9259958565


main()
