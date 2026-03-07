"""unique parcial soft delete

Reemplaza las constraints UNIQUE simples por índices únicos parciales
(WHERE estado = TRUE) para que el soft delete no bloquee la reutilización
de valores únicos en registros nuevos.

Revision ID: f3e8a1b2c4d5
Revises: 60fd4d3c2751
Create Date: 2026-03-07

"""

from alembic import op

revision = "f3e8a1b2c4d5"
down_revision = "60fd4d3c2751"
branch_labels = None
depends_on = None


def upgrade():
    # ── clientes.identificacion ───────────────────────────────────────────
    op.drop_constraint("clientes_identificacion_key", "clientes", type_="unique")
    op.execute(
        """
        CREATE UNIQUE INDEX uq_clientes_identificacion_activo
        ON clientes (identificacion)
        WHERE estado = TRUE
        """
    )

    # ── proveedores.nit ───────────────────────────────────────────────────
    op.drop_constraint("proveedores_nit_key", "proveedores", type_="unique")
    op.execute(
        """
        CREATE UNIQUE INDEX uq_proveedores_nit_activo
        ON proveedores (nit)
        WHERE estado = TRUE
        """
    )

    # ── productos.codigo_barras ───────────────────────────────────────────
    op.drop_constraint("productos_codigo_barras_key", "productos", type_="unique")
    op.execute(
        """
        CREATE UNIQUE INDEX uq_productos_codigo_barras_activo
        ON productos (codigo_barras)
        WHERE estado = TRUE AND codigo_barras IS NOT NULL
        """
    )

    # ── usuarios.username ─────────────────────────────────────────────────
    op.drop_constraint("usuarios_username_key", "usuarios", type_="unique")
    op.execute(
        """
        CREATE UNIQUE INDEX uq_usuarios_username_activo
        ON usuarios (username)
        WHERE estado = TRUE
        """
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS uq_clientes_identificacion_activo")
    op.create_unique_constraint(
        "clientes_identificacion_key", "clientes", ["identificacion"]
    )

    op.execute("DROP INDEX IF EXISTS uq_proveedores_nit_activo")
    op.create_unique_constraint("proveedores_nit_key", "proveedores", ["nit"])

    op.execute("DROP INDEX IF EXISTS uq_productos_codigo_barras_activo")
    op.create_unique_constraint(
        "productos_codigo_barras_key", "productos", ["codigo_barras"]
    )

    op.execute("DROP INDEX IF EXISTS uq_usuarios_username_activo")
    op.create_unique_constraint("usuarios_username_key", "usuarios", ["username"])
