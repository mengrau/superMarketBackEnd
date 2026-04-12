"""Excepciones de dominio y aplicación para la API SuperMarket."""

from dataclasses import dataclass
from typing import Any


@dataclass
class AppError(Exception):
    """Excepción base de negocio para la API."""

    message: str
    status_code: int
    code: str = "APP_ERROR"
    details: Any = None


class BadRequestError(AppError):
    """Error de solicitud inválida (HTTP 400)."""

    def __init__(self, message: str, details: Any = None):
        """Inicializa una instancia de BadRequestError."""
        super().__init__(
            message=message,
            status_code=400,
            code="BAD_REQUEST",
            details=details,
        )


class NotFoundError(AppError):
    """Error cuando un recurso no existe (HTTP 404)."""

    def __init__(self, message: str, details: Any = None):
        """Inicializa una instancia de NotFoundError."""
        super().__init__(
            message=message,
            status_code=404,
            code="NOT_FOUND",
            details=details,
        )


class ConflictError(AppError):
    """Error por conflicto de datos o negocio (HTTP 409)."""

    def __init__(self, message: str, details: Any = None):
        """Inicializa una instancia de ConflictError."""
        super().__init__(
            message=message,
            status_code=409,
            code="CONFLICT",
            details=details,
        )


class UnauthorizedError(AppError):
    """Error de autenticación o autorización (HTTP 401)."""

    def __init__(self, message: str = "No autenticado", details: Any = None):
        """Inicializa una instancia de UnauthorizedError."""
        super().__init__(
            message=message,
            status_code=401,
            code="UNAUTHORIZED",
            details=details,
        )


AppException = AppError
