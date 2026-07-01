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
    assert payload["host"] == "127.0.0.1"
    assert isinstance(payload["command"], list)


def test_runtime_builds_llama_server_command():
    command = runtime_manager.build_command(RuntimeStartRequest(model_path="../Models/QW.gguf", port=8090))

    assert command[1] == "-m"
    assert command[-2:] == ["--port", "8090"]
    assert command[3:5] == ["--host", "127.0.0.1"]
