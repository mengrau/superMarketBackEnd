from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime



class UsuarioBase(BaseModel):
    username: str
    id_rol: UUID
    estado: bool = True



class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=6)



class UsuarioUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    id_rol: UUID | None = None
    estado: bool | None = None



class UsuarioResponse(UsuarioBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime | None = None

    model_config = {
        "from_attributes": True
    }