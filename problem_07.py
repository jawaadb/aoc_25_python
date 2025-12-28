import numpy as np
from helpers import load_text


def load(fp, remove_empty=False):
    arr = np.array(list(map(list, load_text(fp).split())))
    return arr[~np.all(arr == ".", axis=1)] if remove_empty else arr


def solve_1(mat: np.ndarray):
    count = 0

    for prev, cur in zip(mat[:-1], mat[1:]):
        beam_next = (prev == "S") | (prev == "|")

        # continuation
        cur[beam_next & (cur == ".")] = "|"

        # splitting
        active_splitters = beam_next & (cur == "^")
        count += np.sum(active_splitters)
        cur[
            np.hstack([active_splitters[1:], False])
            | np.hstack([False, active_splitters[:-1]]) & (cur == ".")
        ] = "|"

    return count


def disp(mat: np.ndarray, mat_beam=None):
    mat = mat.copy()
    if mat_beam is not None:
        mat[mat_beam & (mat != "^")] = "|"
    print("\n".join(["".join(l) for l in mat]))


def t_add(t0: tuple[int], t1: tuple[int]):
    return (t0[0] + t1[0], t0[1] + t1[1])


memo: dict[tuple[int, int], int] = {}


def split_count(mat: np.ndarray, coord: tuple[int, int]) -> int:
    assert isinstance(coord, tuple)

    # memoisation
    if coord in memo:
        return memo[coord]

    if coord[0] == mat.shape[0] - 1:
        ret_val = 1
    elif mat[*coord] == "." or mat[*coord] == "S":
        ret_val = split_count(mat, t_add(coord, (1, 0)))
    elif mat[*coord] == "^":
        assert mat[*t_add(coord, (0, -1))] == "."
        assert mat[*t_add(coord, (0, 1))] == "."
        ret_val = split_count(mat, t_add(coord, (0, -1))) + split_count(
            mat, t_add(coord, (0, 1))
        )
    else:
        raise ValueError

    memo[coord] = ret_val
    return ret_val


def solve_2(mat: np.ndarray) -> int:
    assert np.all(mat[-1, :] == "."), "Expected bottom row empty"
    assert np.all(mat[:, 0] == "."), "Expected left column empty"
    assert np.all(mat[:, -1] == "."), "Expected right column empty"
    cnt = split_count(mat, (0, np.arange(mat.shape[1])[mat[0, :] == "S"][0]))
    return cnt


def main():
    assert solve_1(load("p07_example.txt")) == 21
    assert solve_1(load("p07_data.txt")) == 1581

    assert solve_2(load("p07_example.txt")) == 40
    assert solve_2(load("p07_data.txt")) == 73007003089792


main()
