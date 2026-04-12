"""Endpoints HTTP para el recurso factura."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.exceptions import BadRequestError, NotFoundError
from crud.factura_crud import FacturaCRUD
from core.config import get_db
from models import (
    DetalleFacturaCreate,
    DetalleFacturaRead,
    FacturaCreate,
    FacturaRead,
    FacturaUpdate,
)

router = APIRouter()


@router.post("/", response_model=FacturaRead, status_code=201)
def create(factura: FacturaCreate, db: Session = Depends(get_db)):
    """Ejecuta create."""
    crud = FacturaCRUD(db)
    try:
        nueva_factura = crud.crear_factura(
            id_cliente=factura.id_cliente,
            id_empleado=factura.id_empleado,
            id_sucursal=factura.id_sucursal,
            metodo_pago=factura.metodo_pago,
        )
        for detalle in factura.detalles:
            crud.agregar_detalle(
                id_factura=nueva_factura.id,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
            )
        db.refresh(nueva_factura)
        return nueva_factura
    except ValueError as e:
        raise BadRequestError(str(e))


@router.get("/", response_model=List[FacturaRead])
def list_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Ejecuta list all."""
    crud = FacturaCRUD(db)
    return crud.obtener_facturas(skip=skip, limit=limit)


@router.get("/cliente/{cliente_id}", response_model=List[FacturaRead])
def get_by_cliente(
    cliente_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Ejecuta get by cliente."""
    crud = FacturaCRUD(db)
    return crud.obtener_facturas_por_cliente(
        id_cliente=cliente_id, skip=skip, limit=limit
    )


@router.get("/sucursal/{sucursal_id}", response_model=List[FacturaRead])
def get_by_sucursal(
    sucursal_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Ejecuta get by sucursal."""
    crud = FacturaCRUD(db)
    return crud.obtener_facturas_por_sucursal(
        id_sucursal=sucursal_id, skip=skip, limit=limit
    )


@router.get("/{factura_id}", response_model=FacturaRead)
def get_one(factura_id: UUID, db: Session = Depends(get_db)):
    """Ejecuta get one."""
    crud = FacturaCRUD(db)
    factura = crud.obtener_factura(factura_id)
    if not factura:
        raise NotFoundError("Factura no encontrada")
    return factura


@router.put("/{factura_id}", response_model=FacturaRead)
def update(factura_id: UUID, datos: FacturaUpdate, db: Session = Depends(get_db)):
    """Ejecuta update."""
    crud = FacturaCRUD(db)
    try:
        factura = crud.actualizar_factura(
            factura_id, **datos.model_dump(exclude_unset=True)
        )
        if not factura:
            raise NotFoundError("Factura no encontrada")
        return factura
    except ValueError as e:
        raise BadRequestError(str(e))


@router.patch("/{factura_id}/anular", response_model=FacturaRead)
def anular(factura_id: UUID, db: Session = Depends(get_db)):
    """Ejecuta anular."""
    crud = FacturaCRUD(db)
    factura = crud.anular_factura(factura_id)
    if not factura:
        raise NotFoundError("Factura no encontrada")
    return factura


@router.post(
    "/{factura_id}/detalles", response_model=DetalleFacturaRead, status_code=201
)
def add_detalle(
    factura_id: UUID, detalle: DetalleFacturaCreate, db: Session = Depends(get_db)
):
    """Agrega un detalle a una factura y recalcula su total."""
    crud = FacturaCRUD(db)
    try:
        return crud.agregar_detalle(
            id_factura=factura_id,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
        )
    except ValueError as e:
        raise BadRequestError(str(e))


@router.get("/{factura_id}/detalles", response_model=List[DetalleFacturaRead])
def get_detalles(factura_id: UUID, db: Session = Depends(get_db)):
    """Lista todos los detalles de una factura."""
    crud = FacturaCRUD(db)
    if not crud.obtener_factura(factura_id):
        raise NotFoundError("Factura no encontrada")
    return crud.obtener_detalles_por_factura(factura_id)


@router.get("/detalles/{detalle_id}", response_model=DetalleFacturaRead)
def get_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un detalle específico por su UUID."""
    crud = FacturaCRUD(db)
    detalle = crud.obtener_detalle(detalle_id)
    if not detalle:
        raise NotFoundError("Detalle no encontrado")
    return detalle


@router.delete("/detalles/{detalle_id}")
def delete_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Elimina un detalle y descuenta su valor del total de la factura."""
    crud = FacturaCRUD(db)
    ok = crud.eliminar_detalle(detalle_id)
    if not ok:
        raise NotFoundError("Detalle no encontrado")
    return {"mensaje": "Detalle eliminado correctamente"}
