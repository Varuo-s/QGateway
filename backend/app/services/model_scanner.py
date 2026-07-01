from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from backend.app.config.settings import get_settings


class ScannedModel(TypedDict):
    name: str
    size_bytes: int
    path: str
    format: str


def scan_models() -> list[ScannedModel]:
    settings = get_settings()
    models: list[ScannedModel] = []

    for configured_path in settings.models.scan_paths:
        scan_root: Path = settings.resolve_path(configured_path)
        if not scan_root.exists() or not scan_root.is_dir():
            continue

        for model_path in scan_root.rglob("*.gguf"):
            if not model_path.is_file():
                continue
            stat = model_path.stat()
            models.append(
                {
                    "name": model_path.name,
                    "size_bytes": stat.st_size,
                    "path": str(model_path),
                    "format": "GGUF",
                }
            )

    return sorted(models, key=lambda item: item["name"].lower())
