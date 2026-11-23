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

    # 3. Tabla de analítica y visitas web
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitas_web (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_hora TEXT,
        fecha_dia TEXT,
        origen TEXT,
        pagina TEXT,
        dispositivo TEXT,
        user_agent TEXT,
        ip_hash TEXT
    );
    """)

    # Columnas opcionales para retargeting inteligente y referidos
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
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN referido_por INTEGER DEFAULT NULL;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN premio_referidos_otorgado INTEGER DEFAULT 0;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN aviso_renovacion_enviado INTEGER DEFAULT 0;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN provincia_favorita TEXT;")
    except Exception:
        pass

    # 4. Tabla de referidos y afiliados virales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS referidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inviter_id INTEGER,
        invited_id INTEGER UNIQUE,
        fecha TEXT,
        recompensa_entregada INTEGER DEFAULT 0
    );
    """)

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
    SET suscripcion_activa = 1, plan = ?, fecha_fin_suscripcion = ?, aviso_renovacion_enviado = 0
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

def registrar_referido(inviter_id: int, invited_id: int) -> Dict:
    """
    Registra que un nuevo usuario (invited_id) se unió gracias a (inviter_id).
    Evita auto-invitaciones y duplicados.
    Retorna el estado de la operación y el total acumulado por el invitador.
    """
    if inviter_id == invited_id:
        return {"valido": False, "motivo": "auto_invitacion"}

    conn = obtener_conexion()
    cursor = conn.cursor()

    # Comprobar si ya existe en la tabla de referidos
    cursor.execute("SELECT inviter_id FROM referidos WHERE invited_id = ?;", (invited_id,))
    existe = cursor.fetchone()
    if existe:
        conn.close()
        return {"valido": False, "motivo": "ya_referido"}

    ahora = datetime.now().isoformat()
    try:
        cursor.execute("""
        INSERT INTO referidos (inviter_id, invited_id, fecha, recompensa_entregada)
        VALUES (?, ?, ?, 0);
        """, (inviter_id, invited_id, ahora))

        cursor.execute("""
        UPDATE usuarios SET referido_por = ? WHERE user_id = ?;
        """, (inviter_id, invited_id))

        # Contar cuántos referidos lleva el invitador
        cursor.execute("SELECT COUNT(*) FROM referidos WHERE inviter_id = ?;", (inviter_id,))
        total_referidos = cursor.fetchone()[0]

        cursor.execute("SELECT premio_referidos_otorgado FROM usuarios WHERE user_id = ?;", (inviter_id,))
        fila_user = cursor.fetchone()
        premio_otorgado = (fila_user[0] == 1) if fila_user else False

        conn.commit()
        conn.close()

        desbloquea_premio = (total_referidos >= 3) and (not premio_otorgado)

        return {
            "valido": True,
            "total_referidos": total_referidos,
            "desbloquea_premio": desbloquea_premio
        }
    except Exception as e:
        conn.close()
        return {"valido": False, "motivo": str(e)}

def obtener_estadisticas_referidos(user_id: int) -> Dict:
    """Devuelve los referidos conseguidos por un usuario y si ya ha cobrado su mes VIP gratis."""
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM referidos WHERE inviter_id = ?;", (user_id,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT premio_referidos_otorgado, suscripcion_activa, fecha_fin_suscripcion FROM usuarios WHERE user_id = ?;", (user_id,))
    row = cursor.fetchone()
    premio = False
    vip_activo = False
    fecha_fin = None
    if row:
        premio = bool(row[0])
        vip_activo = bool(row[1])
        fecha_fin = row[2]

    conn.close()
    return {
        "total_referidos": total,
        "premio_otorgado": premio,
        "faltan": max(0, 3 - total),
        "vip_activo": vip_activo,
        "fecha_fin": fecha_fin
    }

def marcar_premio_referidos_entregado(user_id: int):
    """Marca en la ficha del usuario que ya se le entregó su mes gratis por referidos."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET premio_referidos_otorgado = 1 WHERE user_id = ?;", (user_id,))
    cursor.execute("UPDATE referidos SET recompensa_entregada = 1 WHERE inviter_id = ?;", (user_id,))
    conn.commit()
    conn.close()

def obtener_usuarios_para_recordatorio_renovacion() -> List[Dict]:
    """Devuelve usuarios activos cuya suscripción vence en los próximos 3 días y no han sido avisados."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now()
    limite_aviso = (ahora + timedelta(days=3)).isoformat()
    ahora_iso = ahora.isoformat()

    cursor.execute("""
    SELECT user_id, first_name, username, plan, fecha_fin_suscripcion
    FROM usuarios
    WHERE suscripcion_activa = 1
      AND fecha_fin_suscripcion <= ?
      AND fecha_fin_suscripcion > ?
      AND (aviso_renovacion_enviado = 0 OR aviso_renovacion_enviado IS NULL);
    """, (limite_aviso, ahora_iso))

    filas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return filas

def marcar_aviso_renovacion_enviado(user_id: int):
    """Marca que ya se avisó al usuario sobre el vencimiento próximo de su suscripción."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET aviso_renovacion_enviado = 1 WHERE user_id = ?;", (user_id,))
    conn.commit()
    conn.close()

def procesar_suscripciones_vencidas() -> List[Dict]:
    """Detecta suscripciones que han llegado a su fecha fin y las pasa a estado inactivo."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora_iso = datetime.now().isoformat()
    cursor.execute("""
    SELECT user_id, first_name, username, plan
    FROM usuarios
    WHERE suscripcion_activa = 1
      AND fecha_fin_suscripcion < ?;
    """, (ahora_iso,))
    vencidos = [dict(row) for row in cursor.fetchall()]

    if vencidos:
        cursor.execute("""
        UPDATE usuarios
        SET suscripcion_activa = 0
        WHERE suscripcion_activa = 1
          AND fecha_fin_suscripcion < ?;
        """, (ahora_iso,))
        conn.commit()
    conn.close()
    return vencidos

def guardar_provincia_favorita(user_id: int, provincia: str):
    """Guarda la provincia preferida del usuario para enviarle alertas personalizadas."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios 
        SET provincia_favorita = ?
        WHERE user_id = ?;
    """, (provincia, user_id))
    conn.commit()
    conn.close()

def obtener_provincia_favorita(user_id: int) -> Optional[str]:
    """Obtiene la provincia configurada por el usuario."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT provincia_favorita FROM usuarios WHERE user_id = ?;", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] else None

def obtener_usuarios_por_provincia(provincia: str) -> List[int]:
    """Devuelve los IDs de los usuarios que han activado alertas para esa provincia."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id FROM usuarios 
        WHERE LOWER(provincia_favorita) = LOWER(?);
    """, (provincia,))
    filas = cursor.fetchall()
    conn.close()
    return [f[0] for f in filas]

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

def registrar_visita_web(origen: str = "directo", pagina: str = "/", dispositivo: str = "movil", user_agent: str = "", ip_hash: str = ""):
    """Registra una visita en la web de forma anónima y en tiempo real."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    ahora = datetime.now()
    fecha_hora = ahora.isoformat()
    fecha_dia = ahora.strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO visitas_web (fecha_hora, fecha_dia, origen, pagina, dispositivo, user_agent, ip_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (fecha_hora, fecha_dia, origen[:50], pagina[:100], dispositivo[:50], user_agent[:250], ip_hash[:64]))
    conn.commit()
    conn.close()

def obtener_metricas_visitas() -> Dict:
    """Calcula las métricas de visitas web del día de hoy y totales."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    hoy = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT count(*) FROM visitas_web WHERE fecha_dia = ?", (hoy,))
    visitas_hoy = cursor.fetchone()[0]

    cursor.execute("SELECT count(DISTINCT ip_hash) FROM visitas_web WHERE fecha_dia = ? AND ip_hash != ''", (hoy,))
    unicas_hoy = cursor.fetchone()[0]

    cursor.execute("SELECT count(*) FROM visitas_web")
    visitas_sesion = cursor.fetchone()[0]

    # Cargar acumulado base persistente para que jamás se reinicie al desplegar
    acumulado_base = 2480
    try:
        hist_file = Path(__file__).resolve().parent / "visitas_historico.json"
        if hist_file.exists():
            with open(hist_file, "r", encoding="utf-8") as hf:
                data_h = json.load(hf)
                acumulado_base = data_h.get("acumulado_base", acumulado_base)
    except Exception:
        pass

    visitas_total = acumulado_base + visitas_sesion

    cursor.execute("""
        SELECT origen, count(*) as c FROM visitas_web
        WHERE fecha_dia = ?
        GROUP BY origen ORDER BY c DESC LIMIT 5
    """, (hoy,))
    origenes_hoy = {row["origen"]: row["c"] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT dispositivo, count(*) as c FROM visitas_web
        WHERE fecha_dia = ?
        GROUP BY dispositivo ORDER BY c DESC LIMIT 5
    """, (hoy,))
    dispositivos_hoy = {row["dispositivo"]: row["c"] for row in cursor.fetchall()}

    conn.close()
    return {
        "visitas_hoy": visitas_hoy,
        "unicas_hoy": unicas_hoy if unicas_hoy > 0 else visitas_hoy,
        "visitas_total": visitas_total,
        "origenes_hoy": origenes_hoy,
        "dispositivos_hoy": dispositivos_hoy
    }

if __name__ == "__main__":
    inicializar_bd()
