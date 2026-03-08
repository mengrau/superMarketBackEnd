"""agregar id_sucursal a compras_proveedor

Revision ID: a1b2c3d4e5f6
Revises: f3e8a1b2c4d5
Create Date: 2026-03-08

"""

from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = "5ecd53c3b7e6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "compras_proveedor",
        sa.Column(
            "id_sucursal",
            sa.UUID(),
            sa.ForeignKey("sucursales.id"),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("compras_proveedor", "id_sucursal")
