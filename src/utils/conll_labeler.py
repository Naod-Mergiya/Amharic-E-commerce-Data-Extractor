import re
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from ..utils.text_preprocessor import tokenize

_PRICE_RE = re.compile(r"(\d[\d,\.]*)(?:\s*)(ብር|birr|Birr|እብር)?")

_LOCATION_TOKENS = {
    "አዲስ", "አበባ", "ቦሌ", "Bole", "BOL", "Megenagna", "Mexico", "መግናኛ", "መክሲኮ",
}


def _label_price(tokens: List[str]) -> List[str]:
    labels = ["O"] * len(tokens)
    for i, t in enumerate(tokens):
        if _PRICE_RE.fullmatch(t):
            labels[i] = "B-PRICE"
    return labels


def _label_location(tokens: List[str]) -> List[str]:
    labels = ["O"] * len(tokens)
    for i, tok in enumerate(tokens):
        if tok in _LOCATION_TOKENS:
            labels[i] = "B-LOC"
    return labels


def label_sentence(text: str) -> List[Tuple[str, str]]:
    tokens = tokenize(text)
    price_labels = _label_price(tokens)
    loc_labels = _label_location(tokens)

    final = []
    for tok, p_lbl, l_lbl in zip(tokens, price_labels, loc_labels):
        if p_lbl != "O":
            final.append((tok, p_lbl))
        elif l_lbl != "O":
            final.append((tok, l_lbl))
        else:
            final.append((tok, "O"))
    return final


def dataframe_to_conll(df: pd.DataFrame, text_col: str, max_rows: int = 40) -> List[str]:
    lines: List[str] = []
    subset = df.head(max_rows)
    for msg in subset[text_col]:
        for token, lbl in label_sentence(str(msg)):
            lines.append(f"{token}\t{lbl}")
        lines.append("")  # blank line between messages
    return lines


def main():
    # find repository root (two levels up: .../src/labeling → repo)
    repo_root = Path(__file__).resolve().parents[2]
    csv_path = repo_root / "data" / "preview_messages.csv"
    if not csv_path.exists():
        # create tiny placeholder so the pipeline can still run in demo mode
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        csv_path.write_text("text\ntest message\n", encoding="utf-8")
        print(f"[warn] {csv_path} was missing – created a 1-row placeholder.\n"
              "       Run the ingestion pipeline to replace it with real data.")
    df = pd.read_csv(csv_path)
    out_lines = dataframe_to_conll(df, text_col="text", max_rows=40)
    out_dir = repo_root / "data" / "labels"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "subset.conll"
    out_file.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Wrote {out_file} with {len(out_lines)} lines")


if __name__ == "__main__":
    main()
