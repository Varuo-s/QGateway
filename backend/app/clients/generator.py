from __future__ import annotations

import json
from typing import Literal, TypedDict

from backend.app.config.settings import get_settings
from backend.app.services.model_scanner import scan_models

ConfigFormat = Literal["json", "toml", "yaml"]


class ClientConfig(TypedDict):
    id: str
    name: str
    format: ConfigFormat
    filename: str
    content: str


def _base_url() -> str:
    gateway = get_settings().gateway
    return f"http://{gateway.host}:{gateway.port}/v1"


def _model_id() -> str:
    models = scan_models()
    if models:
        return models[0]["name"]
    return get_settings().resolve_path(get_settings().runtime.model_path).name


def _json(data: dict[str, object]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _toml(data: dict[str, object]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, str):
            lines.append(f'{key} = "{value}"')
        else:
            lines.append(f"{key} = {json.dumps(value)}")
    return "\n".join(lines) + "\n"


def _yaml(data: dict[str, object]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for child_key, child_value in value.items():
                lines.append(f"  {child_key}: {child_value}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def generate_client_configs() -> list[ClientConfig]:
    base_url = _base_url()
    model = _model_id()
    api_key = "qgateway-local"

    openai_sdk = {
        "base_url": base_url,
        "api_key": api_key,
        "model": model,
    }
    codex = {
        "model": model,
        "model_provider": "qgateway",
        "providers": {
            "qgateway": {
                "name": "QGateway",
                "base_url": base_url,
                "env_key": "QGATEWAY_API_KEY",
                "wire_api": "responses",
            }
        },
    }
    cline = {
        "apiProvider": "openai-compatible",
        "openAiBaseUrl": base_url,
        "openAiApiKey": api_key,
        "openAiModelId": model,
    }
    continue_config = {
        "models": [
            {
                "title": "QGateway",
                "provider": "openai",
                "model": model,
                "apiBase": base_url,
                "apiKey": api_key,
            }
        ]
    }

    return [
        {"id": "openai-sdk", "name": "OpenAI SDK", "format": "json", "filename": "openai-sdk.json", "content": _json(openai_sdk)},
        {"id": "codex", "name": "Codex", "format": "toml", "filename": "codex-qgateway.toml", "content": _toml(codex)},
        {"id": "cline", "name": "Cline", "format": "json", "filename": "cline-qgateway.json", "content": _json(cline)},
        {"id": "continue", "name": "Continue", "format": "yaml", "filename": "continue-qgateway.yaml", "content": _yaml(continue_config)},
    ]
