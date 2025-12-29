import numpy as np
from numpy.linalg import norm
from helpers import load_text


def load(fp) -> np.ndarray:
    return np.int64(
        [list(map(int, l.split(","))) for l in load_text(fp).strip().split("\n")]
    )


def dist(pa: np.ndarray, pb: np.ndarray):
    return norm(pb - pa)


def calc_dist_mat(pts: np.ndarray):
    dist_mat = np.zeros((pts.shape[0], pts.shape[0]), dtype=np.float64)
    for i, pa in enumerate(pts):
        for j, pb in enumerate(pts):
            dist_mat[i, j] = dist(pa, pb)

    assert np.all(dist_mat == dist_mat.transpose())
    return dist_mat


def find_shortest_not_connected(dist_mat: np.ndarray, conn_mat: np.ndarray):
    assert dist_mat.shape[0] == dist_mat.shape[1]
    assert conn_mat.shape == dist_mat.shape

    min_val = dist_mat[(np.eye(dist_mat.shape[0]) != 1) & (~conn_mat)].min()

    iyy, ixx = np.indices(dist_mat.shape)

    found = dist_mat == min_val
    coords = np.vstack([iyy[found], ixx[found]]).transpose()
    return coords


def connect_shortest(dist_mat: np.ndarray, conn_mat: np.ndarray):
    coords = find_shortest_not_connected(dist_mat, conn_mat)
    for pt in coords:
        conn_mat[*pt] = True


def is_distilled(conn_mat: np.ndarray) -> bool:
    for i, irow in enumerate(conn_mat):
        for j, jrow in enumerate(conn_mat):
            if i == j:
                continue
            if np.any(irow & jrow):
                return False
    return True


def calc_connection_sets(conn_mat: np.ndarray):
    while not is_distilled(conn_mat):
        for i, irow in enumerate(conn_mat):
            for j, jrow in enumerate(conn_mat):
                if i == j:
                    continue
                if not np.any(irow & jrow):
                    continue
                jrow[:] = irow | jrow
                irow[:] = False

    indices = np.arange(conn_mat.shape[1])
    groups = sorted(
        filter(lambda g: np.size(g) != 0, (indices[row] for row in conn_mat)),
        key=np.size,
        reverse=True,
    )
    return list(groups)


def solve(fp, num_of_connections, num_to_take):
    arr = load(fp)

    dist_mat = calc_dist_mat(arr)
    conn_mat = np.eye(arr.shape[0], dtype=np.bool)

    for _ in range(num_of_connections):
        connect_shortest(dist_mat, conn_mat)

    groups = calc_connection_sets(conn_mat)
    return np.prod(list(map(np.size, groups[:num_to_take])))


def main():
    assert solve("p08_example.txt", 10, 3) == 40
    assert solve("p08_data.txt", 1000, 3) == 123234


main()
