from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.config.settings import get_settings
from backend.app.runtime.manager import RuntimeStartRequest, runtime_manager
from backend.app.services.model_scanner import format_size, parse_quantization, scan_models


def test_health_api_returns_ok():
    client = TestClient(app)
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "QGateway"


def test_settings_loads_project_config():
    settings = get_settings()

    assert settings.gateway.port == 4000
    assert settings.project_root.name == "QGateway"
    assert settings.runtime.provider == "llama.cpp"


def test_model_scanner_returns_list_without_required_directories():
    result = scan_models()

    assert isinstance(result, list)
    assert all(Path(item["path"]).suffix.lower() == ".gguf" for item in result)


def test_model_scanner_parses_quantization_from_name():
    assert parse_quantization("qwen2.5-7b-instruct-q4_k_m.gguf") == "Q4_K_M"
    assert parse_quantization("llama-8b.Q8_0.gguf") == "Q8_0"
    assert parse_quantization("model.gguf") is None


def test_model_scanner_formats_sizes():
    assert format_size(512) == "512 B"
    assert format_size(1024) == "1.00 KB"


def test_models_scan_api_shape():
    client = TestClient(app)
    response = client.get("/api/v1/models/scan")

    assert response.status_code == 200
    payload = response.json()
    assert "count" in payload
    assert "scan_time" in payload
    assert "models" in payload


def test_runtime_status_api_shape():
    client = TestClient(app)
    response = client.get("/api/v1/runtime/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "llama.cpp"
    assert payload["state"] in {"stopped", "running", "error"}
    assert payload["host"] in {"127.0.0.1", "0.0.0.0"}
    assert isinstance(payload["command"], list)


def test_runtime_builds_llama_server_command():
    command = runtime_manager.build_command(RuntimeStartRequest(model_path="../Models/QW.gguf", host="0.0.0.0", port=8999))

    assert command[1] == "-m"
    assert "-a" in command
    assert "Qwythos-9B" in command
    assert command[command.index("-ngl") + 1] == "all"
    assert command[command.index("-c") + 1] == "16384"
    assert command[command.index("--flash-attn") + 1] == "auto"
    assert command[command.index("--reasoning") + 1] == "off"
    assert command[command.index("--reasoning-format") + 1] == "none"
    assert command[command.index("--log-colors") + 1] == "off"
    assert command[command.index("--host") + 1] == "0.0.0.0"
    assert command[command.index("--port") + 1] == "8999"


def test_openai_models_api_shape():
    client = TestClient(app)
    response = client.get("/v1/models")

    assert response.status_code == 200
    payload = response.json()
    assert payload["object"] == "list"
    assert isinstance(payload["data"], list)
    assert payload["data"]
    assert payload["data"][0]["object"] == "model"


def test_openai_responses_api_proxies_chat_completion(monkeypatch):
    import httpx
    from backend.app.openai import routes as openai_routes

    captured = {}

    class FakeClient:
        def __init__(self, timeout):
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def post(self, url, json):
            captured["url"] = url
            captured["json"] = json
            return httpx.Response(200, request=httpx.Request("POST", url), json={"choices": [{"message": {"content": "hello from runtime"}}]})

    monkeypatch.setattr(openai_routes.httpx, "Client", FakeClient)
    client = TestClient(app)
    response = client.post("/v1/responses", json={"input": "hello", "temperature": 0.1})

    assert response.status_code == 200
    payload = response.json()
    assert payload["object"] == "response"
    assert payload["status"] == "completed"
    assert payload["output_text"] == "hello from runtime"
    assert captured["url"].endswith("/v1/chat/completions")
    assert captured["json"]["messages"] == [{"role": "user", "content": "hello"}]


def test_clients_configs_api_shape():
    client = TestClient(app)
    response = client.get("/api/v1/clients/configs")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 5
    ids = {item["id"] for item in payload["configs"]}
    assert {"openai-sdk", "codex", "cline", "claude-code", "continue"}.issubset(ids)
    assert all("http://127.0.0.1:4000/v1" in item["content"] for item in payload["configs"])


def test_runtime_settings_update_api():
    client = TestClient(app)
    original = get_settings().runtime.model_dump()
    response = client.put("/api/v1/settings/runtime", json={"host": "0.0.0.0", "port": 8999, "reasoning": "off"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["runtime"]["host"] == "0.0.0.0"
    assert payload["runtime"]["port"] == 8999

    client.put("/api/v1/settings/runtime", json=original)

