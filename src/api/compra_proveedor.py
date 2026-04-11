"""Endpoints HTTP para el recurso compra proveedor."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.compra_proveedor_crud import CompraProveedorCRUD
from core.config import get_db
from models import (
    CompraProveedorCreate,
    CompraProveedorRead,
    CompraProveedorUpdate,
    DetalleCompraCreate,
    DetalleCompraRead,
)

router = APIRouter()


@router.post("/", response_model=CompraProveedorRead, status_code=201)
def create(compra: CompraProveedorCreate, db: Session = Depends(get_db)):
    crud = CompraProveedorCRUD(db)
    try:
        nueva_compra = crud.crear_compra(
            id_proveedor=compra.id_proveedor,
            id_sucursal=compra.id_sucursal,
        )
        for detalle in compra.detalles:
            crud.agregar_detalle(
                id_compra=nueva_compra.id,
                id_producto=detalle.id_producto,
                cantidad=detalle.cantidad,
                precio_compra=detalle.precio_compra,
            )
        db.refresh(nueva_compra)
        return nueva_compra
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CompraProveedorRead])
def list_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    crud = CompraProveedorCRUD(db)
    return crud.obtener_compras(skip=skip, limit=limit)


@router.get("/proveedor/{proveedor_id}", response_model=List[CompraProveedorRead])
def get_by_proveedor(
    proveedor_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    crud = CompraProveedorCRUD(db)
    return crud.obtener_compras_por_proveedor(
        id_proveedor=proveedor_id, skip=skip, limit=limit
    )


@router.get("/{compra_id}", response_model=CompraProveedorRead)
def get_one(compra_id: UUID, db: Session = Depends(get_db)):
    crud = CompraProveedorCRUD(db)
    compra = crud.obtener_compra(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra


@router.put("/{compra_id}", response_model=CompraProveedorRead)
def update(
    compra_id: UUID, datos: CompraProveedorUpdate, db: Session = Depends(get_db)
):
    crud = CompraProveedorCRUD(db)
    try:
        compra = crud.actualizar_compra(
            compra_id, **datos.model_dump(exclude_unset=True)
        )
        if not compra:
            raise HTTPException(status_code=404, detail="Compra no encontrada")
        return compra
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{compra_id}/anular", response_model=CompraProveedorRead)
def anular(compra_id: UUID, db: Session = Depends(get_db)):
    crud = CompraProveedorCRUD(db)
    compra = crud.anular_compra(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra


@router.post("/{compra_id}/detalles", response_model=DetalleCompraRead)
def add_detalle(
    compra_id: UUID, detalle: DetalleCompraCreate, db: Session = Depends(get_db)
):
    """Agrega un detalle a una compra y recalcula su total."""
    crud = CompraProveedorCRUD(db)
    try:
        return crud.agregar_detalle(
            id_compra=compra_id,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_compra=detalle.precio_compra,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{compra_id}/detalles", response_model=List[DetalleCompraRead])
def get_detalles(compra_id: UUID, db: Session = Depends(get_db)):
    """Lista todos los detalles de una compra a proveedor."""
    crud = CompraProveedorCRUD(db)
    if not crud.obtener_compra(compra_id):
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return crud.obtener_detalles_por_compra(compra_id)


@router.get("/detalles/{detalle_id}", response_model=DetalleCompraRead)
def get_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un detalle específico de compra por su UUID."""
    crud = CompraProveedorCRUD(db)
    detalle = crud.obtener_detalle(detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.delete("/detalles/{detalle_id}")
def delete_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Elimina un detalle de compra y descuenta su valor del total."""
    crud = CompraProveedorCRUD(db)
    ok = crud.eliminar_detalle(detalle_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return {"mensaje": "Detalle eliminado correctamente"}
