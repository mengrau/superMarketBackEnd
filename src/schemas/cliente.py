from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str
    tipo_identificacion: str
    identificacion: str
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[bool] = True

class ClienteCreate(ClienteBase):
    id_usuario_creacion: UUID

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo_identificacion: Optional[str] = None
    identificacion: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[bool] = None
    id_usuario_edicion: UUID

class ClienteResponse(ClienteBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]

    class Config:
        from_attributes = True