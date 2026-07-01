from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

from backend.app.config.settings import get_settings

_QUANTIZATION_PATTERN = re.compile(r"(?:^|[.-])((?:IQ|Q)\d(?:_[A-Z0-9]+)*)(?:[.-]|$)", re.IGNORECASE)


class ScannedModel(TypedDict):
    name: str
    size_bytes: int
    size_label: str
    path: str
    relative_path: str
    format: str
    quantization: str | None
    modified_at: str


def format_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.2f} {units[unit_index]}"


def parse_quantization(file_name: str) -> str | None:
    match = _QUANTIZATION_PATTERN.search(Path(file_name).stem)
    if not match:
        return None
    return match.group(1).upper()


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
            try:
                relative_path = str(model_path.relative_to(settings.project_root))
            except ValueError:
                relative_path = str(model_path)

            models.append(
                {
                    "name": model_path.name,
                    "size_bytes": stat.st_size,
                    "size_label": format_size(stat.st_size),
                    "path": str(model_path),
                    "relative_path": relative_path,
                    "format": "GGUF",
                    "quantization": parse_quantization(model_path.name),
                    "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                }
            )

    return sorted(models, key=lambda item: item["name"].lower())
