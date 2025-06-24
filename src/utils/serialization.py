"""Simple helpers for reading/writing jsonl files."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping, Any


def dump_jsonl(path: Path, records: Iterable[Mapping[str, Any]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for rec in records:
            json_record = json.dumps(rec, ensure_ascii=False)
            f.write(json_record + "\n")
