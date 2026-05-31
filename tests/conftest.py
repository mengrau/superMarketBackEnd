"""Configuracion compartida para las pruebas de la API."""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SSL_MODE", "disable")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-with-at-least-32-bytes")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import app


@pytest.fixture
def client():
    """Crear un cliente HTTP de pruebas para FastAPI."""
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
