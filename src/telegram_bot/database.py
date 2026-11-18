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

    # Columnas opcionales para retargeting inteligente
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN descargo_guia INTEGER DEFAULT 0;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN fecha_guia TEXT;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN retargeting_enviado INTEGER DEFAULT 0;")
    except Exception:
        pass

    # 3. Tabla de pagos y transacciones de Stripe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagos_stripe (
        session_id TEXT PRIMARY KEY,
        user_id INTEGER,
        customer_email TEXT,
        amount_total REAL,
        currency TEXT,
        plan TEXT,
        fecha_pago TEXT,
        estado TEXT DEFAULT 'completado'
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

def registrar_descarga_guia(user_id: int):
    """Registra la fecha en que el usuario descargó la guía para retargeting."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().isoformat()
    cursor.execute("""
    UPDATE usuarios 
    SET descargo_guia = 1, fecha_guia = ?
    WHERE user_id = ?;
    """, (ahora, user_id))
    conn.commit()
    conn.close()

def obtener_usuarios_para_retargeting() -> List[Dict]:
    """Busca usuarios que descargaron la guía hace más de 20h, no son VIP y no recibieron retargeting."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT user_id, username, first_name 
    FROM usuarios 
    WHERE descargo_guia = 1 
      AND suscripcion_activa = 0 
      AND retargeting_enviado = 0
      AND datetime(fecha_guia, '+20 hours') <= datetime('now');
    """)
    filas = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return filas

def marcar_retargeting_enviado(user_id: int):
    """Marca que el usuario ya recibió el mensaje de seguimiento para no molestarle más."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE usuarios 
    SET retargeting_enviado = 1 
    WHERE user_id = ?;
    """, (user_id,))
    conn.commit()
    conn.close()

def registrar_pago_stripe(session_id: str, user_id: Optional[int], email: str, amount: float, currency: str, plan: str):
    """Guarda en SQLite la confirmación del pago recibido vía Webhook de Stripe."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now().isoformat()
    cursor.execute("""
    INSERT OR REPLACE INTO pagos_stripe (session_id, user_id, customer_email, amount_total, currency, plan, fecha_pago, estado)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'completado');
    """, (session_id, user_id, email, amount, currency, plan, ahora))
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

def obtener_metricas_globales() -> Dict:
    """Calcula las métricas operativas del negocio para el comando /stats del administrador."""
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios;")
    total_usuarios = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE DATE(fecha_alta) = DATE('now');")
    usuarios_hoy = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE suscripcion_activa = 1;")
    vip_activos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alertas_enviadas;")
    total_alertas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alertas_enviadas WHERE DATE(fecha_envio) = DATE('now');")
    alertas_hoy = cursor.fetchone()[0]

    cursor.execute("SELECT plan, COUNT(*) FROM usuarios WHERE suscripcion_activa = 1 GROUP BY plan;")
    desglose_planes = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()

    return {
        "total_usuarios": total_usuarios,
        "usuarios_hoy": usuarios_hoy,
        "vip_activos": vip_activos,
        "total_alertas": total_alertas,
        "alertas_hoy": alertas_hoy,
        "desglose_planes": desglose_planes
    }

if __name__ == "__main__":
    inicializar_bd()
