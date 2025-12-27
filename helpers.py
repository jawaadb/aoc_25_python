from pathlib import Path


def load_text(fname: str) -> str:
    with open(Path(f"data/{fname}"), "r", encoding="utf-8") as f:
        return "".join(f.readlines())
