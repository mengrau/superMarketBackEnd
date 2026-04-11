"""
Manejadores globales de errores para FastAPI.
"""

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from core.errors import AppError


def _build_error_payload(
    request: Request,
    message: str,
    code: str,
    details: Any = None,
) -> dict:
    payload = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
        "path": request.url.path,
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content=_build_error_payload(
                request=request,
                message=exc.message,
                code=exc.code,
                details=exc.details,
            ),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        detail = exc.detail
        message = detail if isinstance(detail, str) else "Error HTTP"
        return JSONResponse(
            status_code=exc.status_code,
            content=_build_error_payload(
                request=request,
                message=message,
                code=f"HTTP_{exc.status_code}",
                details=None if isinstance(detail, str) else detail,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content=_build_error_payload(
                request=request,
                message="Datos de entrada inválidos",
                code="VALIDATION_ERROR",
                details=exc.errors(),
            ),
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=409,
            content=_build_error_payload(
                request=request,
                message="Conflicto de integridad en base de datos",
                code="CONFLICT",
                details=str(exc.orig) if exc.orig else str(exc),
            ),
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content=_build_error_payload(
                request=request,
                message=str(exc),
                code="BAD_REQUEST",
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=_build_error_payload(
                request=request,
                message="Error interno del servidor",
                code="INTERNAL_SERVER_ERROR",
            ),
        )
