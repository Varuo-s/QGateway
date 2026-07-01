from __future__ import annotations

import time
import uuid
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException

from backend.app.config.settings import get_settings
from backend.app.openai.schemas import ModelList, OpenAIModel, ResponsesOutputMessage, ResponsesOutputText, ResponsesRequest, ResponsesResponse
from backend.app.services.model_scanner import scan_models

router = APIRouter(prefix="/v1")


def _runtime_base_url() -> str:
    runtime = get_settings().runtime
    return f"http://{runtime.host}:{runtime.port}"


def _default_model_id() -> str:
    runtime = get_settings().runtime
    if runtime.model_path:
        return get_settings().resolve_path(runtime.model_path).name
    models = scan_models()
    if models:
        return models[0]["name"]
    return "qgateway-local-model"


def _messages_from_responses_request(request: ResponsesRequest) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if request.instructions:
        messages.append({"role": "system", "content": request.instructions})

    if isinstance(request.input, str):
        messages.append({"role": "user", "content": request.input})
        return messages

    for item in request.input:
        if isinstance(item, dict):
            role = str(item.get("role", "user"))
            content = item.get("content", "")
        else:
            role = item.role
            content = item.content
        messages.append({"role": role, "content": str(content)})
    return messages


def _extract_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices") or []
    if not choices:
        return ""
    first = choices[0]
    message = first.get("message") or {}
    content = message.get("content")
    if content is None:
        content = first.get("text", "")
    return str(content)


@router.get("/models", response_model=ModelList)
def list_models() -> ModelList:
    scanned = scan_models()
    if scanned:
        models = [OpenAIModel(id=item["name"]) for item in scanned]
    else:
        models = [OpenAIModel(id=_default_model_id())]
    return ModelList(data=models)


@router.post("/responses", response_model=ResponsesResponse)
def create_response(request: ResponsesRequest) -> ResponsesResponse:
    if request.stream:
        raise HTTPException(status_code=400, detail="Streaming responses are not implemented in Alpha 0.4")

    model_id = request.model or _default_model_id()
    payload: dict[str, Any] = {
        "model": model_id,
        "messages": _messages_from_responses_request(request),
        "stream": False,
    }
    if request.temperature is not None:
        payload["temperature"] = request.temperature
    if request.top_p is not None:
        payload["top_p"] = request.top_p
    if request.max_output_tokens is not None:
        payload["max_tokens"] = request.max_output_tokens

    try:
        with httpx.Client(timeout=120.0) as client:
            upstream = client.post(f"{_runtime_base_url()}/v1/chat/completions", json=payload)
            upstream.raise_for_status()
            upstream_payload = upstream.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Runtime request failed: {exc}") from exc

    text = _extract_text(upstream_payload)
    return ResponsesResponse(
        id=f"resp_{uuid.uuid4().hex}",
        created_at=int(time.time()),
        model=model_id,
        output=[ResponsesOutputMessage(id=f"msg_{uuid.uuid4().hex}", content=[ResponsesOutputText(text=text)])],
        output_text=text,
    )
