from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ResponseInputMessage(BaseModel):
    role: str = "user"
    content: str


class ResponsesRequest(BaseModel):
    model: str | None = None
    input: str | list[ResponseInputMessage] | list[dict[str, Any]]
    instructions: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    max_output_tokens: int | None = None
    stream: bool = False


class OpenAIModel(BaseModel):
    id: str
    object: Literal["model"] = "model"
    created: int = 0
    owned_by: str = "qgateway"


class ModelList(BaseModel):
    object: Literal["list"] = "list"
    data: list[OpenAIModel]


class ResponsesOutputText(BaseModel):
    type: Literal["output_text"] = "output_text"
    text: str


class ResponsesOutputMessage(BaseModel):
    id: str
    type: Literal["message"] = "message"
    role: Literal["assistant"] = "assistant"
    content: list[ResponsesOutputText]


class ResponsesResponse(BaseModel):
    id: str
    object: Literal["response"] = "response"
    created_at: int
    status: Literal["completed"] = "completed"
    model: str
    output: list[ResponsesOutputMessage]
    output_text: str
