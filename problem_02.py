import math
from typing import Callable
from functools import partial
from helpers import load_text


def load_ranges(fp) -> list[tuple[int, int]]:
    return [
        tuple(map(int, t.split("-"))) for t in "".join(load_text(fp)).strip().split(",")
    ]


def has_two_repeats(n: int):
    # if odd number of digits, not repeated
    num_digits = math.floor(math.log10(n)) + 1
    if num_digits % 2 == 1:
        return False

    n_part = n // (10 ** (num_digits // 2))
    n_full = n_part * (10 ** (num_digits // 2) + 1)

    return n == n_full


def find_invalids(rng: tuple[int, int], is_invalid: Callable):
    return filter(is_invalid, range(rng[0], rng[1] + 1))


def sum_invalids(fp, is_invalid: Callable):
    return sum(
        map(
            sum,
            (
                map(
                    partial(find_invalids, is_invalid=is_invalid),
                    load_ranges(fp),
                )
            ),
        )
    )


def main():
    assert sum_invalids("p02_example.txt", has_two_repeats) == 1227775554
    assert sum_invalids("p02_data.txt", has_two_repeats) == 19128774598


main()
