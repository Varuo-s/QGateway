from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class GatewaySettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 4000
    version: str = "alpha-0.3"


class LogSettings(BaseModel):
    level: str = "INFO"
    file: str = "logs/qgateway.log"


class ModelSettings(BaseModel):
    scan_paths: list[str] = Field(default_factory=lambda: ["../Models", "Models", "models", "AI/Models"])


class LauncherSettings(BaseModel):
    executables: list[str] = Field(default_factory=lambda: ["llama-server", "ollama", "lmstudio"])


class RuntimeSettings(BaseModel):
    provider: str = "llama.cpp"
    executable: str = "../llama-server.exe"
    host: str = "127.0.0.1"
    port: int = 8080
    model_path: str = "../Models/QW.gguf"


class Settings(BaseModel):
    gateway: GatewaySettings = Field(default_factory=GatewaySettings)
    logs: LogSettings = Field(default_factory=LogSettings)
    models: ModelSettings = Field(default_factory=ModelSettings)
    launcher: LauncherSettings = Field(default_factory=LauncherSettings)
    runtime: RuntimeSettings = Field(default_factory=RuntimeSettings)
    project_root: Path

    def resolve_path(self, value: str) -> Path:
        path = Path(value).expanduser()
        if path.is_absolute():
            return path
        return self.project_root / path


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__)).resolve()
    for parent in [current, *current.parents]:
        if (parent / "config.yaml").exists():
            return parent
    return Path.cwd().resolve()


def load_settings(config_path: Path | None = None) -> Settings:
    root = find_project_root(config_path or Path(__file__))
    path = config_path or root / "config.yaml"
    raw: dict[str, Any] = {}
    if path.exists():
        with path.open("r", encoding="utf-8") as config_file:
            raw = yaml.safe_load(config_file) or {}
    return Settings(**raw, project_root=root)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()
