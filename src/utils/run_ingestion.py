"""CLI script to start Telegram data ingestion."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow running from project root without installing as package
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from ingestion.telegram_client import TelegramIngestor  # noqa: E402  pylint: disable=C0413

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Start ingestion from Telegram channels")
    parser.add_argument(
        "channels",
        nargs="*",
        help="Optional list of Telegram channel usernames or IDs (without @). Defaults to predefined constants.",
    )
    args = parser.parse_args()

    # Import here to avoid unnecessary dependency when running unit tests
    from constants.channels import CHANNEL_USERNAMES  # noqa: E402  pylint: disable=C0413

    channels = args.channels or CHANNEL_USERNAMES
    ingestor = TelegramIngestor(channels=channels)
    ingestor.run()


if __name__ == "__main__":
    main()
