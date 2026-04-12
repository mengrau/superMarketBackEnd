"""Agregar columnas empleados

Revision ID: 5ecd53c3b7e6
Revises: f3e8a1b2c4d5
Create Date: 2026-03-08 12:18:32.302211

"""

from alembic import op
import sqlalchemy as sa


revision = "5ecd53c3b7e6"
down_revision = "f3e8a1b2c4d5"
branch_labels = None
depends_on = None


def upgrade():
    """Ejecuta upgrade."""
    op.drop_index(
        "uq_clientes_identificacion_activo",
        table_name="clientes",
        postgresql_where="(estado = true)",
    )
    op.add_column(
        "empleados", sa.Column("nombre", sa.String(length=120), nullable=False)
    )
    op.add_column(
        "empleados",
        sa.Column("tipo_identificacion", sa.String(length=5), nullable=False),
    )
    op.add_column(
        "empleados", sa.Column("identificacion", sa.String(length=50), nullable=False)
    )
    op.add_column(
        "empleados", sa.Column("telefono", sa.String(length=20), nullable=True)
    )
    op.add_column(
        "empleados", sa.Column("direccion", sa.String(length=200), nullable=True)
    )
    op.create_unique_constraint(None, "empleados", ["identificacion"])
    op.drop_index(
        "uq_productos_codigo_barras_activo",
        table_name="productos",
        postgresql_where="((estado = true) AND (codigo_barras IS NOT NULL))",
    )
    op.drop_index(
        "uq_proveedores_nit_activo",
        table_name="proveedores",
        postgresql_where="(estado = true)",
    )
    op.drop_index(
        "uq_usuarios_username_activo",
        table_name="usuarios",
        postgresql_where="(estado = true)",
    )


def downgrade():
    """Ejecuta downgrade."""
    op.create_index(
        "uq_usuarios_username_activo",
        "usuarios",
        ["username"],
        unique=False,
        postgresql_where="(estado = true)",
    )
    op.create_index(
        "uq_proveedores_nit_activo",
        "proveedores",
        ["nit"],
        unique=False,
        postgresql_where="(estado = true)",
    )
    op.create_index(
        "uq_productos_codigo_barras_activo",
        "productos",
        ["codigo_barras"],
        unique=False,
        postgresql_where="((estado = true) AND (codigo_barras IS NOT NULL))",
    )
    op.drop_constraint(None, "empleados", type_="unique")
    op.drop_column("empleados", "direccion")
    op.drop_column("empleados", "telefono")
    op.drop_column("empleados", "identificacion")
    op.drop_column("empleados", "tipo_identificacion")
    op.drop_column("empleados", "nombre")
    op.create_index(
        "uq_clientes_identificacion_activo",
        "clientes",
        ["identificacion"],
        unique=False,
        postgresql_where="(estado = true)",
    )
