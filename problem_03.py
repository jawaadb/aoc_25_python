from helpers import load_text


def max_joltage(bank: str):
    lst = list(map(int, bank))
    lmax = max(lst[:-1])
    idx_lmax = lst.index(lmax)
    rmax = max(lst[idx_lmax + 1 :])
    return lmax * 10 + rmax


def max_12_digit_joltage(bank: str):
    bank = list(map(int, bank))

    res: list[int] = []
    i_left = -1
    for i in range(11, -1, -1):
        m = bank[i_left + 1 : None if i == 0 else -i]

        n_max = max(m)
        i_left = m.index(n_max) + i_left + 1
        res.append(n_max)

    return sum(r * 10**p for r, p in zip(res, range(11, -1, -1)))


def main():
    banks = load_text("p03_example.txt").strip().split("\n")
    assert sum(map(max_joltage, banks)) == 357
    assert sum(map(max_12_digit_joltage, banks)) == 3121910778619

    banks = load_text("p03_data.txt").strip().split("\n")

    # Part 1
    assert sum(map(max_joltage, banks)) == 17321
    # Part 2
    assert sum(map(max_12_digit_joltage, banks)) == 171989894144198


main()
