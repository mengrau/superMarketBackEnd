"""Pruebas del endpoint raiz de la API."""


def test_root_endpoint_ok(client):
    """Valida que la API responde con sus metadatos principales."""
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload.get("mensaje") == "Bienvenido a SuperMarket API"
    assert payload.get("version") == "1.0.0"
    assert "endpoints" in payload
    assert "Clientes" in payload["endpoints"]
