import numpy as np
from helpers import load_text


def load(fp):
    return np.array(list(map(list, load_text(fp).split())))


def solve(mat: np.ndarray):
    split_count = 0

    for i, (prev, cur) in enumerate(zip(mat[:-1], mat[1:])):
        beam_next = (prev == "S") | (prev == "|")

        # continuation
        cur[beam_next & (cur == ".")] = "|"

        # splitting
        active_splitters = beam_next & (cur == "^")
        split_count += np.sum(active_splitters)
        cur[
            np.hstack([active_splitters[1:], False])
            | np.hstack([False, active_splitters[:-1]]) & (cur == ".")
        ] = "|"

    # print("\n".join(["".join(l) for l in mat]))
    return split_count


def main():
    assert solve(load("p07_example.txt")) == 21
    assert solve(load("p07_data.txt")) == 1581


main()
