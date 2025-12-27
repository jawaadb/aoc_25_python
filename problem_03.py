from helpers import load_text


def max_joltage(bank: str):
    lst = list(map(int, bank))
    lmax = max(lst[:-1])
    idx_lmax = lst.index(lmax)
    rmax = max(lst[idx_lmax + 1 :])
    return lmax * 10 + rmax


def main():

    # Part 1
    banks = load_text("p03_example.txt").strip().split("\n")
    assert sum(map(max_joltage, banks)) == 357

    banks = load_text("p03_data.txt").strip().split("\n")
    assert sum(map(max_joltage, banks)) == 17321


main()
