"""Compatibilidad: manejadores movidos a core.error_handlers."""

from core.error_handlers import register_exception_handlers  # noqa: F401

__all__ = ["register_exception_handlers"]
