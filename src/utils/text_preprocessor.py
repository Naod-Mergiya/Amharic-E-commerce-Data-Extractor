"""Utilities for preprocessing Amharic text."""

import regex as re
from typing import List

# Ethiopic and ASCII punctuation to strip
PUNCT_PATTERN = re.compile(r"[\p{P}\p{S}\u1360-\u137F\u200B]+", re.UNICODE)

ETHIOPIC_LETTERS = r"\p{Script=Ethiopic}+"
LATIN_LETTERS = r"\p{Script=Latin}+"
DIGITS = r"\p{Nd}+"
TOKEN_PATTERN = re.compile(f"({ETHIOPIC_LETTERS}|{LATIN_LETTERS}|{DIGITS})", re.UNICODE)


def normalize(text: str) -> str:
    """Remove punctuation and redundant whitespace."""
    text = PUNCT_PATTERN.sub("", text)
    return " ".join(text.split())


def tokenize(text: str) -> List[str]:
    """Split into Ethiopic, Latin word, or digit tokens using unicode script info."""
    return TOKEN_PATTERN.findall(text)


def preprocess(text: str) -> List[str]:
    return tokenize(normalize(text))
