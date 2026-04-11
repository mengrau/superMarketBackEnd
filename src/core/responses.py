"""Utilidades para respuestas JSON homogéneas de la API."""

from typing import Any


def success_response(data: Any, message: str | None = None) -> dict[str, Any]:
    """Construir una respuesta de éxito con estructura estándar."""
    return {
        "success": True,
        "data": data,
        "message": message,
    }


def error_response(
    code: str,
    message: str,
    details: Any = None,
    path: str | None = None,
) -> dict[str, Any]:
    """Construir una respuesta de error con estructura estándar."""
    payload: dict[str, Any] = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if details is not None:
        payload["error"]["details"] = details
    if path:
        payload["path"] = path
    return payload
