"""
Base de datos SQLite local para gestión de usuarios, membresías y alertas enviadas.
Coste 0 € y cero dependencias de servidores externos.
"""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "radar_usuarios.db"
DB_PATH.parent.mkdir(exist_ok=True)

def obtener_conexion() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_bd():
    """Crea las tablas necesarias si no existen."""
    conn = obtener_conexion()
    cursor = conn.cursor()

    # 1. Tabla de usuarios y suscripciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        suscripcion_activa INTEGER DEFAULT 0,
        plan TEXT DEFAULT 'free',
        fecha_alta TEXT,
        fecha_fin_suscripcion TEXT,
        stripe_session_id TEXT
    );
    """)

    # 2. Tabla de histórico de alertas enviadas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alertas_enviadas (
        id_subasta TEXT PRIMARY KEY,
        titulo TEXT,
        precio_salida TEXT,
        fecha_envio TEXT
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos SQLite inicializada en data/radar_usuarios.db")

def registrar_o_actualizar_usuario(user_id: int, username: Optional[str], first_name: str):
    """Guarda al usuario al hacer /start si no existía."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO usuarios (user_id, username, first_name, fecha_alta)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        username=excluded.username,
        first_name=excluded.first_name;
    """, (user_id, username or "", first_name, ahora))
    conn.commit()
    conn.close()

def activar_suscripcion_vip(user_id: int, plan: str = "mensual_15e", dias: int = 30):
    """Activa el pase VIP por 30 días tras confirmar el pago."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    fecha_fin = (datetime.now() + timedelta(days=dias)).isoformat()
    cursor.execute("""
    UPDATE usuarios
    SET suscripcion_activa = 1, plan = ?, fecha_fin_suscripcion = ?
    WHERE user_id = ?;
    """, (plan, fecha_fin, user_id))
    conn.commit()
    conn.close()
    print(f"⭐ Suscripción VIP activada para el usuario {user_id} hasta {fecha_fin}")

def desactivar_suscripcion_vip(user_id: int):
    """Cancela el acceso VIP (por baja voluntaria o fallo de pago)."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE usuarios
    SET suscripcion_activa = 0, plan = 'free'
    WHERE user_id = ?;
    """, (user_id,))
    conn.commit()
    conn.close()
    print(f"❌ Suscripción VIP cancelada para el usuario {user_id}")

def obtener_estado_usuario(user_id: int) -> Optional[Dict]:
    """Consulta si el usuario es VIP y cuándo le caduca la suscripción."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE user_id = ?;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def registrar_alerta_enviada(id_subasta: str, titulo: str, precio_salida: str):
    """Marca una subasta como ya notificada para no duplicarla."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().isoformat()
    cursor.execute("""
    INSERT OR IGNORE INTO alertas_enviadas (id_subasta, titulo, precio_salida, fecha_envio)
    VALUES (?, ?, ?, ?);
    """, (id_subasta, titulo, precio_salida, ahora))
    conn.commit()
    conn.close()

def ya_fue_enviada(id_subasta: str) -> bool:
    """Comprueba si una subasta ya se envió a los canales."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM alertas_enviadas WHERE id_subasta = ?;", (id_subasta,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

if __name__ == "__main__":
    inicializar_bd()
