from pathlib import Path


def load_text(fname: str):
    with open(Path(f"data/{fname}"), "r", encoding="utf-8") as f:
        return f.readlines()
