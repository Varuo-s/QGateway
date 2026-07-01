from __future__ import annotations

import logging
from pathlib import Path

from backend.app.config.settings import get_settings


def configure_logging() -> logging.Logger:
    settings = get_settings()
    logger = logging.getLogger("qgateway")
    if logger.handlers:
        return logger

    logger.setLevel(settings.logs.level.upper())
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    log_path: Path = settings.resolve_path(settings.logs.file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    base_logger = configure_logging()
    if not name:
        return base_logger
    return logging.getLogger(f"qgateway.{name}")
