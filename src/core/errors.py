"""Compatibilidad: excepciones movidas a core.exceptions."""

from core.exceptions import (  # noqa: F401
    AppError,
    AppException,
    BadRequestError,
    ConflictError,
    NotFoundError,
    UnauthorizedError,
)

__all__ = [
    "AppError",
    "AppException",
    "BadRequestError",
    "ConflictError",
    "NotFoundError",
    "UnauthorizedError",
]
