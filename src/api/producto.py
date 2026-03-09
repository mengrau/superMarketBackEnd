from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database.config import get_db
from models import ProductoCreate, ProductoRead, ProductoUpdate
from crud.producto_crud import ProductoCRUD

router = APIRouter()


@router.post("/", response_model=ProductoRead, status_code=201)
def create(producto: ProductoCreate, db: Session = Depends(get_db)):
    crud = ProductoCRUD(db)
    try:
        return crud.crear_producto(
            nombre=producto.nombre,
            precio_venta=producto.precio_venta,
            codigo_barras=producto.codigo_barras,
            fecha_vencimiento=producto.fecha_vencimiento,
            id_tipo=producto.id_tipo,
            id_proveedor=producto.id_proveedor,
            id_usuario_creacion=getattr(producto, "id_usuario_creacion", None),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProductoRead])
def list_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    crud = ProductoCRUD(db)
    return crud.obtener_productos(skip=skip, limit=limit)


@router.get("/{producto_id}", response_model=ProductoRead)
def get_by_id(producto_id: UUID, db: Session = Depends(get_db)):
    crud = ProductoCRUD(db)
    producto = crud.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=ProductoRead)
def update(producto_id: UUID, datos: ProductoUpdate, db: Session = Depends(get_db)):
    crud = ProductoCRUD(db)
    try:
        producto = crud.actualizar_producto(
            producto_id,
            id_usuario_edicion=getattr(datos, "id_usuario_edicion", None),
            **datos.model_dump(exclude_unset=True),
        )
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{producto_id}", response_model=ProductoRead)
def delete(producto_id: UUID, db: Session = Depends(get_db)):
    crud = ProductoCRUD(db)
    producto = crud.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    crud.eliminar_producto(producto_id)
    return producto
