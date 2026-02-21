from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from entities import Usuario


class Empleado(Usuario):
    __tablename__ = "empleados"

    id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), primary_key=True)

    cargo = Column(String(80))
    salario = Column(String(50))

    __mapper_args__ = {"polymorphic_identity": "empleado"}

    def __repr__(self):
        return f"<Empleado {self.username}>"
