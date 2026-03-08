from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from entities import Usuario


class Empleado(Usuario):
    __tablename__ = "empleados"

    id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), primary_key=True)

    # Datos personales
    nombre = Column(String(120), nullable=False)
    tipo_identificacion = Column(String(5), unique=False, nullable=False)
    identificacion = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))

    # Datos laborales
    cargo = Column(String(80))
    salario = Column(String(50))

    __mapper_args__ = {"polymorphic_identity": "empleado"}

    def __repr__(self):
        return f"<Empleado {self.nombre}>"
