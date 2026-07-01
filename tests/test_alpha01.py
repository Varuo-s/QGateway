from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.config.settings import get_settings
from backend.app.services.model_scanner import scan_models


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
