from itertools import accumulate
from helpers import load_text


def load_deltas(fp):
    return [
        {"L": -1, "R": 1}[l[0]] * int(l[1:]) for l in load_text(fp).strip().split("\n")
    ]


def solve_part1(fp):
    positions = accumulate([50] + load_deltas(fp), lambda a, b: (a + b) % 100)
    return len(list(filter(lambda v: v == 0, positions)))


def solve_part2(fp):
    deltas = load_deltas(fp)

    def move(p0, delta) -> tuple[int, int]:
        assert 0 <= p0 < 100
        assert delta != 0

        p1 = p0 + delta

        if delta > 0:
            zero_crossings = p1 // 100
        else:
            zero_crossings = -(p1 // 100) + (p1 % 100 == 0) - (p0 % 100 == 0)

        return p1 % 100, zero_crossings

    zero_count = 0
    positions = [50]
    for d in deltas:
        p1, cnt = move(positions[-1], d)
        zero_count += cnt
        positions.append(p1)

    return zero_count


def main():
    # Part 1
    assert solve_part1("p01_example.txt") == 3
    assert solve_part1("p01_data.txt") == 1135

    # Part 2
    assert solve_part2("p01_example.txt") == 6
    assert solve_part2("p01_data.txt") == 6558


main()
