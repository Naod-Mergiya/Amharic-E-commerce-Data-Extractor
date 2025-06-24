"""Alternate ingestion runner without dotenv dependency.

Usage:
    python fetch/01_simple_ingestion.py  # defaults to CHANNEL_USERNAMES
    python fetch/01_simple_ingestion.py customChannel1 customChannel2

Expects API_ID and API_HASH to be filled in `src/credentials.py`.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Ensure src/ is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from credentials import API_ID, API_HASH  # noqa: E402  pylint: disable=C0413
from constants.channels import CHANNEL_USERNAMES  # noqa: E402  pylint: disable=C0413
from ingestion.telegram_client import TelegramIngestor  # noqa: E402  pylint: disable=C0413

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def main():
    if API_ID is None or API_HASH is None:
        raise RuntimeError("Fill API_ID and API_HASH in src/credentials.py before running.")

    parser = argparse.ArgumentParser(description="Start ingestion from Telegram channels (no dotenv)")
    parser.add_argument("channels", nargs="*", help="Channel usernames without @. Defaults to constant list.")
    args = parser.parse_args()

    channels = args.channels or CHANNEL_USERNAMES
    ingestor = TelegramIngestor(channels=channels)
    ingestor.run()


if __name__ == "__main__":
    main()
