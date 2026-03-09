"""
Centraliza todas las llamadas HTTP a la FastAPI del SuperMarket.

Todas las funciones lanzan RuntimeError con el detalle de error de la API si la
respuesta HTTP no es exitosa, o si no se puede conectar al servidor.

El BASE_URL por defecto es http://localhost:8000 y puede sobreescribirse con la
variable de entorno HTTP_CLIENT_BASE_URL.
"""

import os
import requests

BASE_URL = os.getenv("HTTP_CLIENT_BASE_URL", "http://localhost:8000")

_CONNECTION_ERROR_MSG = (
    f"No se puede conectar a la API en {BASE_URL}. "
    "¿Está corriendo el servidor? Usa la opción 13 del menú para iniciarlo."
)


def _raise_for_status(resp: requests.Response) -> None:
    if not resp.ok:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        raise RuntimeError(detail)


def get(path: str, params: dict = None):
    """GET {BASE_URL}{path}. Retorna el JSON parseado."""
    try:
        resp = requests.get(f"{BASE_URL}{path}", params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(_CONNECTION_ERROR_MSG)
    _raise_for_status(resp)
    return resp.json()


def post(path: str, body: dict):
    """POST {BASE_URL}{path} con body JSON. Retorna el JSON parseado."""
    try:
        resp = requests.post(f"{BASE_URL}{path}", json=body, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(_CONNECTION_ERROR_MSG)
    _raise_for_status(resp)
    return resp.json()


def put(path: str, body: dict):
    """PUT {BASE_URL}{path} con body JSON. Retorna el JSON parseado."""
    try:
        resp = requests.put(f"{BASE_URL}{path}", json=body, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(_CONNECTION_ERROR_MSG)
    _raise_for_status(resp)
    return resp.json()


def patch(path: str, body: dict = None, params: dict = None):
    """PATCH {BASE_URL}{path}. Acepta body JSON y/o query params. Retorna el JSON parseado."""
    try:
        resp = requests.patch(f"{BASE_URL}{path}", json=body, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(_CONNECTION_ERROR_MSG)
    _raise_for_status(resp)
    return resp.json()


def delete(path: str):
    """DELETE {BASE_URL}{path}. Retorna el JSON parseado."""
    try:
        resp = requests.delete(f"{BASE_URL}{path}", timeout=10)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(_CONNECTION_ERROR_MSG)
    _raise_for_status(resp)
    return resp.json()
