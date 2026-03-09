from typing import List
from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.compra_proveedor_crud import CompraProveedorCRUD
from database.config import get_db
from models import DetalleCompraCreate, DetalleCompraRead

router = APIRouter()


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
