"""init

Revision ID: d4c257c78e3b
Revises:
Create Date: 2026-02-21 00:06:23.646825

"""

from alembic import op
import sqlalchemy as sa


revision = "d4c257c78e3b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Ejecuta upgrade."""
    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nombre", sa.String(length=80), nullable=False),
        sa.Column("descripcion", sa.String(length=250), nullable=True),
        sa.Column("salario", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_table(
        "tipo_productos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("descripcion", sa.String(length=300), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "usuarios",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("id_rol", sa.UUID(), nullable=False),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.Column("tipo", sa.String(length=50), nullable=True),
        sa.Column("id_usuario_creacion", sa.UUID(), nullable=True),
        sa.Column("id_usuario_edicion", sa.UUID(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_rol"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_creacion"],
            ["usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edicion"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "clientes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("tipo_identificacion", sa.String(length=5), nullable=False),
        sa.Column("identificacion", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("telefono", sa.String(length=20), nullable=True),
        sa.Column("direccion", sa.String(length=200), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.Column("id_usuario_creacion", sa.UUID(), nullable=True),
        sa.Column("id_usuario_edicion", sa.UUID(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_usuario_creacion"],
            ["usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edicion"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("identificacion"),
    )
    op.create_table(
        "empleados",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("cargo", sa.String(length=80), nullable=True),
        sa.Column("salario", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "proveedores",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("nit", sa.String(length=50), nullable=False),
        sa.Column("telefono", sa.String(length=20), nullable=True),
        sa.Column("direccion", sa.String(length=200), nullable=True),
        sa.Column("correo", sa.String(length=120), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.Column("id_usuario_creacion", sa.UUID(), nullable=True),
        sa.Column("id_usuario_edicion", sa.UUID(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_usuario_creacion"],
            ["usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edicion"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nit"),
    )
    op.create_table(
        "sucursales",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("direccion", sa.String(length=200), nullable=True),
        sa.Column("gerente", sa.String(length=120), nullable=True),
        sa.Column("telefono", sa.String(length=20), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.Column("id_usuario_creacion", sa.UUID(), nullable=True),
        sa.Column("id_usuario_edicion", sa.UUID(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_usuario_creacion"],
            ["usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edicion"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "compras_proveedor",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=False),
        sa.Column("total_compra", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("id_proveedor", sa.UUID(), nullable=False),
        sa.Column("estado", sa.String(length=30), nullable=True),
        sa.Column("id_usuario_creacion", sa.UUID(), nullable=True),
        sa.Column("id_usuario_edicion", sa.UUID(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_proveedor"],
            ["proveedores.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_creacion"],
            ["usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edicion"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "facturas",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=False),
        sa.Column("total", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("metodo_pago", sa.String(length=80), nullable=True),
        sa.Column("id_cliente", sa.UUID(), nullable=False),
        sa.Column("id_empleado", sa.UUID(), nullable=False),
        sa.Column("id_sucursal", sa.UUID(), nullable=False),
        sa.Column("estado", sa.String(length=30), nullable=True),
        sa.Column("id_usuario_creacion", sa.UUID(), nullable=True),
        sa.Column("id_usuario_edicion", sa.UUID(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_cliente"],
            ["clientes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_empleado"],
            ["empleados.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_sucursal"],
            ["sucursales.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_creacion"],
            ["usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edicion"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "productos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nombre", sa.String(length=200), nullable=False),
        sa.Column("codigo_barras", sa.String(length=100), nullable=True),
        sa.Column("precio_venta", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("fecha_vencimiento", sa.DateTime(), nullable=True),
        sa.Column("id_tipo", sa.UUID(), nullable=True),
        sa.Column("id_proveedor", sa.UUID(), nullable=True),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.Column("id_usuario_creacion", sa.UUID(), nullable=True),
        sa.Column("id_usuario_edicion", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_proveedor"],
            ["proveedores.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_tipo"],
            ["tipo_productos.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_creacion"],
            ["usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edicion"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("codigo_barras"),
    )
    op.create_table(
        "detalle_compras",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("precio_compra", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("id_compra", sa.UUID(), nullable=False),
        sa.Column("id_producto", sa.UUID(), nullable=False),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_compra"],
            ["compras_proveedor.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_producto"],
            ["productos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "detalle_facturas",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("precio_unitario", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("subtotal", sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column("id_factura", sa.UUID(), nullable=False),
        sa.Column("id_producto", sa.UUID(), nullable=False),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_factura"],
            ["facturas.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_producto"],
            ["productos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "inventarios",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("stock_actual", sa.Integer(), nullable=False),
        sa.Column("stock_minimo", sa.Integer(), nullable=False),
        sa.Column("ubicacion", sa.String(length=200), nullable=True),
        sa.Column("id_producto", sa.UUID(), nullable=False),
        sa.Column("id_sucursal", sa.UUID(), nullable=False),
        sa.Column("estado", sa.Boolean(), nullable=True),
        sa.Column("id_usuario_creacion", sa.UUID(), nullable=True),
        sa.Column("id_usuario_edicion", sa.UUID(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_producto"],
            ["productos.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_sucursal"],
            ["sucursales.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_creacion"],
            ["usuarios.id"],
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario_edicion"],
            ["usuarios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    """Ejecuta downgrade."""
    op.drop_table("inventarios")
    op.drop_table("detalle_facturas")
    op.drop_table("detalle_compras")
    op.drop_table("productos")
    op.drop_table("facturas")
    op.drop_table("compras_proveedor")
    op.drop_table("sucursales")
    op.drop_table("proveedores")
    op.drop_table("empleados")
    op.drop_table("clientes")
    op.drop_table("usuarios")
    op.drop_table("tipo_productos")
    op.drop_table("roles")
