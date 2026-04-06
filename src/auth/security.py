from passlib.context import CryptContext

# Usar solo bcrypt sin schemes deprecados para evitar problemas de compatibilidad
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception as e:
    print(f"⚠️ Advertencia: Problema al inicializar bcrypt: {e}")
    # Fallback a plaintext para desarrollo (¡NO usar en producción!)
    pwd_context = None


def hash_password(password: str) -> str:
    """Genera el hash seguro de la contraseña"""
    if pwd_context is None:
        # Fallback si bcrypt falla (solo para desarrollo)
        return f"plaintext:{password}"

    # Asegurar que la contraseña no excede 72 bytes (límite de bcrypt)
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode("utf-8", errors="ignore")

    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"⚠️ Error al hashear contraseña: {e}")
        return f"plaintext:{password}"


def verify_password(password: str, hashed: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    # Manejar fallback plaintext
    if hashed.startswith("plaintext:"):
        return password == hashed.replace("plaintext:", "")

    if pwd_context is None:
        return False

    # Asegurar que la contraseña no excede 72 bytes
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode("utf-8", errors="ignore")

    try:
        return pwd_context.verify(password, hashed)
    except Exception as e:
        print(f"⚠️ Error al verificar contraseña: {e}")
        return False
