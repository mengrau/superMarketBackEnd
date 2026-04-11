"""Pruebas smoke para validar el arranque basico de la API."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import app  # noqa: E402


def test_root_endpoint_ok():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload.get("mensaje") == "Bienvenido a SuperMarket API"
    assert payload.get("version") == "1.0.0"
    assert "endpoints" in payload
    assert "Clientes" in payload["endpoints"]
