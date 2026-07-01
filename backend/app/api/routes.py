from __future__ import annotations

from time import monotonic

from fastapi import APIRouter

from backend.app.config.settings import get_settings
from backend.app.launcher.detector import detect_launchers
from backend.app.logging.logger import get_logger
from backend.app.services.log_reader import read_recent_logs
from backend.app.services.model_scanner import scan_models

router = APIRouter(prefix="/api/v1")
_started_at = monotonic()
logger = get_logger("api")


@router.get("/health")
def health() -> dict[str, object]:
    settings = get_settings()
    logger.info("health check requested")
    return {
        "status": "ok",
        "service": "QGateway",
        "version": settings.gateway.version,
        "runtime": "running",
        "uptime_seconds": round(monotonic() - _started_at, 3),
    }


@router.get("/settings")
def settings() -> dict[str, object]:
    current = get_settings()
    return {
        "gateway": current.gateway.model_dump(),
        "logs": current.logs.model_dump(),
        "models": current.models.model_dump(),
        "launcher": current.launcher.model_dump(),
    }


@router.get("/models/scan")
def models_scan() -> dict[str, object]:
    models = scan_models()
    return {"count": len(models), "models": models}


@router.get("/launcher/detect")
def launcher_detect() -> dict[str, object]:
    candidates = detect_launchers()
    return {"candidates": candidates}


@router.get("/logs")
def logs(limit: int = 200) -> dict[str, object]:
    bounded_limit = max(1, min(limit, 1000))
    return {"lines": read_recent_logs(bounded_limit)}
