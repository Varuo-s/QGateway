from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.config.settings import get_settings
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
