from __future__ import annotations

from pathlib import Path

from backend.app.config.settings import get_settings


def read_recent_logs(limit: int = 200) -> list[str]:
    settings = get_settings()
    log_path: Path = settings.resolve_path(settings.logs.file)
    if not log_path.exists():
        return []

    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[-limit:]
