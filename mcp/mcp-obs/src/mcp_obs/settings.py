"""Runtime settings for the MCP observability server."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    victorialogs_url: str
    victoriatraces_url: str


def resolve_settings() -> Settings:
    victorialogs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL", "").strip()
    if not victorialogs_url:
        raise RuntimeError(
            "VictoriaLogs URL not configured. Set NANOBOT_VICTORIALOGS_URL."
        )

    victoriatraces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL", "").strip()
    if not victoriatraces_url:
        raise RuntimeError(
            "VictoriaTraces URL not configured. Set NANOBOT_VICTORIATRACES_URL."
        )

    return Settings(
        victorialogs_url=victorialogs_url.rstrip("/"),
        victoriatraces_url=victoriatraces_url.rstrip("/"),
    )
