"""Pruebas del CRUD HTTP de clientes."""

from types import SimpleNamespace
from uuid import uuid4

from core.auth import get_current_active_user
from core.config import get_db
from crud.cliente_crud import ClienteCRUD
from main import app


def _cliente_response(**overrides):
    data = {
        "id": uuid4(),
        "nombre": "Cliente Examen",
        "tipo_identificacion": "CC",
        "identificacion": "123456789",
        "email": "cliente.examen@example.com",
        "telefono": "3001234567",
        "direccion": "Calle 1 # 2-3",
        "estado": True,
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def _auth_user():
    return SimpleNamespace(
        id=uuid4(),
        username="admin",
        id_rol=uuid4(),
        estado=True,
    )


def _override_db():
    yield object()


def test_clientes_rechaza_peticion_sin_token(client):
    """Valida que un endpoint protegido no acepta solicitudes anonimas."""
    response = client.get("/clientes/")

    assert response.status_code == 401


def test_crear_cliente_con_datos_validos(client, monkeypatch):
    """Valida la operacion crear del CRUD de clientes."""

    def fake_create(self, **kwargs):
        return _cliente_response(**kwargs)

    monkeypatch.setattr(ClienteCRUD, "crear_cliente", fake_create)
    app.dependency_overrides[get_db] = _override_db
    app.dependency_overrides[get_current_active_user] = _auth_user

    response = client.post(
        "/clientes/",
        json={
            "nombre": "Cliente Examen",
            "tipo_identificacion": "CC",
            "identificacion": "123456789",
            "email": "cliente.examen@example.com",
            "telefono": "3001234567",
            "direccion": "Calle 1 # 2-3",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["nombre"] == "Cliente Examen"
    assert payload["identificacion"] == "123456789"


def test_listar_clientes_retorna_registros(client, monkeypatch):
    """Valida la operacion listar del CRUD de clientes."""

    def fake_list(self, skip=0, limit=10):
        rows = [_cliente_response(nombre="Cliente listado")]
        return rows[skip : skip + limit]

    monkeypatch.setattr(ClienteCRUD, "obtener_clientes", fake_list)
    app.dependency_overrides[get_db] = _override_db
    app.dependency_overrides[get_current_active_user] = _auth_user

    response = client.get("/clientes/")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["nombre"] == "Cliente listado"


def test_actualizar_cliente_modifica_datos(client, monkeypatch):
    """Valida la operacion actualizar del CRUD de clientes."""
    cliente_id = uuid4()

    def fake_update(self, cliente_id_param, id_usuario_edicion=None, **kwargs):
        assert cliente_id_param == cliente_id
        return _cliente_response(id=cliente_id, nombre=kwargs["nombre"])

    monkeypatch.setattr(ClienteCRUD, "actualizar_cliente", fake_update)
    app.dependency_overrides[get_db] = _override_db
    app.dependency_overrides[get_current_active_user] = _auth_user

    response = client.put(
        f"/clientes/{cliente_id}",
        json={"nombre": "Cliente Actualizado"},
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Cliente Actualizado"


def test_eliminar_cliente_desactiva_registro(client, monkeypatch):
    """Valida la operacion eliminar del CRUD de clientes."""
    cliente_id = uuid4()
    cliente = _cliente_response(id=cliente_id)

    def fake_get(self, cliente_id_param):
        assert cliente_id_param == cliente_id
        return cliente

    def fake_delete(self, cliente_id_param):
        assert cliente_id_param == cliente_id
        cliente.estado = False
        return True

    monkeypatch.setattr(ClienteCRUD, "obtener_cliente", fake_get)
    monkeypatch.setattr(ClienteCRUD, "eliminar_cliente", fake_delete)
    app.dependency_overrides[get_db] = _override_db
    app.dependency_overrides[get_current_active_user] = _auth_user

    response = client.delete(f"/clientes/{cliente_id}")

    assert response.status_code == 200
    assert response.json()["estado"] is False
