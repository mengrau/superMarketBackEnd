from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.errors import BadRequestError, NotFoundError
from crud.inventario_crud import InventarioCRUD
from database.config import get_db
from models import InventarioCreate, InventarioRead, InventarioUpdate

router = APIRouter()


@router.post("/", response_model=InventarioRead, status_code=201)
def create(inventario: InventarioCreate, db: Session = Depends(get_db)):
    crud = InventarioCRUD(db)
    try:
        return crud.crear_inventario(
            id_producto=inventario.id_producto,
            id_sucursal=inventario.id_sucursal,
            stock_actual=inventario.stock_actual,
            stock_minimo=inventario.stock_minimo,
            ubicacion=inventario.ubicacion,
        )
    except ValueError as e:
        raise BadRequestError(str(e))


@router.get("/", response_model=List[InventarioRead])
def list_all(
    skip: int = 0,
    limit: int = 10,
    solo_activos: bool = True,
    db: Session = Depends(get_db),
):
    crud = InventarioCRUD(db)
    return crud.obtener_inventarios(skip=skip, limit=limit, solo_activos=solo_activos)


@router.get("/bajo-minimo", response_model=List[InventarioRead])
def get_bajo_minimo(id_sucursal: Optional[UUID] = None, db: Session = Depends(get_db)):
    """Retorna los inventarios cuyo stock actual está por debajo del stock mínimo."""
    crud = InventarioCRUD(db)
    return crud.obtener_inventarios_bajo_minimo(id_sucursal=id_sucursal)


@router.get("/sucursal/{sucursal_id}", response_model=List[InventarioRead])
def get_by_sucursal(
    sucursal_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    crud = InventarioCRUD(db)
    return crud.obtener_inventarios_por_sucursal(
        id_sucursal=sucursal_id, skip=skip, limit=limit
    )


@router.get("/{inventario_id}", response_model=InventarioRead)
def get_one(inventario_id: UUID, db: Session = Depends(get_db)):
    crud = InventarioCRUD(db)
    inv = crud.obtener_inventario(inventario_id)
    if not inv:
        raise NotFoundError("Inventario no encontrado")
    return inv


@router.put("/{inventario_id}", response_model=InventarioRead)
def update(inventario_id: UUID, datos: InventarioUpdate, db: Session = Depends(get_db)):
    crud = InventarioCRUD(db)
    try:
        inv = crud.actualizar_inventario(
            inventario_id, **datos.model_dump(exclude_unset=True)
        )
        if not inv:
            raise NotFoundError("Inventario no encontrado")
        return inv
    except ValueError as e:
        raise BadRequestError(str(e))


@router.patch("/{inventario_id}/ajustar-stock", response_model=InventarioRead)
def ajustar_stock(inventario_id: UUID, cantidad: int, db: Session = Depends(get_db)):
    """Ajusta el stock del inventario. `cantidad` positiva suma, negativa resta."""
    crud = InventarioCRUD(db)
    try:
        inv = crud.ajustar_stock(inventario_id, cantidad)
        if not inv:
            raise NotFoundError("Inventario no encontrado")
        return inv
    except ValueError as e:
        raise BadRequestError(str(e))


@router.delete("/{inventario_id}", response_model=InventarioRead)
def delete(inventario_id: UUID, db: Session = Depends(get_db)):
    crud = InventarioCRUD(db)
    inv = crud.obtener_inventario(inventario_id)
    if not inv:
        raise NotFoundError("Inventario no encontrado")
    crud.eliminar_inventario(inventario_id)
    return inv
