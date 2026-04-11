"""
Excepciones personalizadas y utilidades para respuestas de error homogéneas.
"""

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
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            message=message,
            status_code=400,
            code="BAD_REQUEST",
            details=details,
        )


class NotFoundError(AppError):
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            message=message,
            status_code=404,
            code="NOT_FOUND",
            details=details,
        )


class ConflictError(AppError):
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            message=message,
            status_code=409,
            code="CONFLICT",
            details=details,
        )


class UnauthorizedError(AppError):
    def __init__(self, message: str = "No autenticado", details: Any = None):
        super().__init__(
            message=message,
            status_code=401,
            code="UNAUTHORIZED",
            details=details,
        )
