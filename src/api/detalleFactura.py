from typing import List
from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.factura_crud import FacturaCRUD
from database.config import get_db
from models import DetalleFacturaCreate, DetalleFacturaRead

router = APIRouter()


@router.post("/{factura_id}/detalles", response_model=DetalleFacturaRead)
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
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{factura_id}/detalles", response_model=List[DetalleFacturaRead])
def get_detalles(factura_id: UUID, db: Session = Depends(get_db)):
    """Lista todos los detalles de una factura."""
    crud = FacturaCRUD(db)
    if not crud.obtener_factura(factura_id):
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return crud.obtener_detalles_por_factura(factura_id)


@router.get("/detalles/{detalle_id}", response_model=DetalleFacturaRead)
def get_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un detalle específico por su UUID."""
    crud = FacturaCRUD(db)
    detalle = crud.obtener_detalle(detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.delete("/detalles/{detalle_id}")
def delete_detalle(detalle_id: UUID, db: Session = Depends(get_db)):
    """Elimina un detalle y descuenta su valor del total de la factura."""
    crud = FacturaCRUD(db)
    ok = crud.eliminar_detalle(detalle_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return {"mensaje": "Detalle eliminado correctamente"}
