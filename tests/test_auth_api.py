"""Pruebas de autenticacion de la API."""

from types import SimpleNamespace
from uuid import uuid4

from core.config import get_db
from crud.usuario_crud import UsuarioCRUD
from main import app


def _auth_user():
    return SimpleNamespace(
        id=uuid4(),
        username="admin",
        id_rol=uuid4(),
        estado=True,
    )


def _override_db():
    yield object()


def test_login_exitoso_devuelve_token(client, monkeypatch):
    """Valida que /auth/login retorna un JWT para credenciales validas."""

    def fake_authenticate(self, username, password):
        assert username == "admin"
        assert password == "admin123"
        return _auth_user()

    monkeypatch.setattr(UsuarioCRUD, "autenticar_usuario", fake_authenticate)
    app.dependency_overrides[get_db] = _override_db

    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["expires_in"] > 0
