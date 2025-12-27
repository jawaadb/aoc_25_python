from helpers import load_text


def load(fp):
    txt = load_text(fp).strip()
    txt_rngs, txt_ids = txt.split("\n\n")
    ranges = [list(map(int, txt.split("-"))) for txt in txt_rngs.split("\n")]
    ranges = [range(r[0], r[1] + 1) for r in ranges]
    ids = list(map(int, txt_ids.split("\n")))
    return ranges, ids


def count_fresh(fp):
    ranges, ids = load(fp)
    fresh_ids = filter(lambda i: any(i in r for r in ranges), ids)
    return len(list(fresh_ids))


def main():
    assert count_fresh("p05_example.txt") == 3
    assert count_fresh("p05_data.txt") == 874


main()
