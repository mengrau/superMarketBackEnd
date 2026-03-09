"""valores de rol de raiz

Revision ID: 60fd4d3c2751
Revises: d4c257c78e3b
Create Date: 2026-03-06 19:53:34.526591

"""

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = "60fd4d3c2751"
down_revision = "d4c257c78e3b"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""
        INSERT INTO roles (id, nombre, descripcion, salario, activo, fecha_creacion)
        VALUES
            ('{uuid.uuid4()}', 'admin', 'Administrador del sistema', 2000000, TRUE, now()),
            ('{uuid.uuid4()}', 'empleado', 'Empleado general', 2000000, TRUE, now())
        """
    )


def downgrade():
    op.execute("DELETE FROM roles WHERE nombre IN ('admin', 'empleado', 'cliente')")
