from collections import namedtuple
import numpy as np
from helpers import load_text

Range = namedtuple("Range", ["min", "max"])


def load(fp):
    txt = load_text(fp).strip()
    txt_rngs, txt_ids = txt.split("\n\n")
    ranges = [list(map(int, txt.split("-"))) for txt in txt_rngs.split("\n")]

    ranges = [Range(min=r[0], max=r[1]) for r in ranges]
    ids = list(map(int, txt_ids.split("\n")))
    return ranges, ids


def is_in_range(value: int, rng: Range) -> bool:
    return rng.min <= value <= rng.max


def count_fresh(fp):
    ranges, ids = load(fp)
    fresh_ids = filter(lambda i: any(is_in_range(i, r) for r in ranges), ids)
    return len(list(fresh_ids))


def are_overlapping(ra: Range, rb: Range) -> bool:
    return not (
        (ra.min < rb.min and ra.max < rb.min) or (ra.min > rb.max and ra.max > rb.max)
    )


def calc_overlap_matrix(ranges: list[Range]):
    assert isinstance(ranges, list)
    assert isinstance(ranges[0], Range)

    mat = np.zeros((len(ranges), len(ranges)), dtype=np.bool)
    for i, ra in enumerate(ranges):
        for j, rb in enumerate(ranges):
            mat[i, j] = are_overlapping(ra, rb)

    assert mat.shape[0] == mat.shape[1]
    assert np.all(mat == mat.transpose()), "Expected symmetry"
    return mat


def combined_range(rngs: list[Range]) -> Range:
    return Range(
        min=min(map(lambda r: r.min, rngs)), max=max(map(lambda r: r.max, rngs))
    )


def reduce_ranges(ranges: list[range]) -> bool:
    mat = calc_overlap_matrix(ranges)

    reduced = False
    for i, row in enumerate(mat):
        if np.sum(row) == 1:
            continue

        idx_overlaps = np.indices(row.shape)[0, row]
        new_rng = combined_range([ranges[i] for i in idx_overlaps])
        for i in idx_overlaps[::-1]:
            ranges.pop(i)
        ranges.append(new_rng)
        reduced = True
        break
    return reduced


def solve(fp):
    ranges, _ = load(fp)

    while True:
        res = reduce_ranges(ranges)
        if res is False:
            break

    return sum(map(lambda r: max(r) - min(r) + 1, ranges))


def main():
    assert count_fresh("p05_example.txt") == 3
    assert count_fresh("p05_data.txt") == 874
    assert solve("p05_example.txt") == 14
    assert solve("p05_data.txt") == 348548952146313


main()
