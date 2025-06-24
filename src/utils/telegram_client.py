"""Telegram client wrapper for data ingestion.

Uses Telethon to connect to Telegram and fetch messages from specified channels.
"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Iterable, List

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.types import Document

from src.config import API_HASH, API_ID, RAW_DATA_DIR, SESSION_NAME
from src.utils.serialization import dump_jsonl

logger = logging.getLogger(__name__)


class TelegramIngestor:
    """Asynchronously fetch messages from Telegram channels."""

    def __init__(self, channels: Iterable[str]):
        self.channels: List[str] = list(channels)
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        self._ready_event = asyncio.Event()

    async def _on_message(self, event: events.NewMessage.Event):  # type: ignore
        message: Message = event.message
        if not message:
            return

        channel = event.chat if event.chat else None
        channel_name = getattr(channel, "title", "unknown") if channel else "unknown"

        logger.info("Got message from %s", channel_name)

        record = {
            "channel": channel_name,
            "sender_id": message.sender_id,
            "message_id": message.id,
            "date": message.date.isoformat(),
            "text": message.text or "",
            "entities": [str(e) for e in message.entities or []],
            "media": self._extract_media_info(message),
        }

        # Persist to disk (append mode)
        out_file = RAW_DATA_DIR / f"{channel_name}.jsonl"
        dump_jsonl(out_file, [record])

    @staticmethod
    def _extract_media_info(message: Message):
        if message.photo:
            return {"type": "photo"}
        if isinstance(message.media, Document):
            return {"type": "document", "mime_type": message.media.mime_type}
        return None

    async def start(self):
        await self.client.start()
        self.client.add_event_handler(self._on_message, events.NewMessage(chats=self.channels))
        logger.info("Telemetry ingestion started for channels: %s", ", ".join(self.channels))
        self._ready_event.set()
        await self.client.run_until_disconnected()

    def run(self):
        asyncio.run(self.start())
