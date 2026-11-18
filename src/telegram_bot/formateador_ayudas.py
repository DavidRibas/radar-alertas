"""
Formateador de Alertas de Ayudas y Subvenciones Públicas
Genera los mensajes ejecutivos para el canal de Telegram (VIP y Free).
"""
import re
import urllib.parse
from datetime import datetime, timedelta, date
from typing import Dict, Tuple

def parsear_fecha_plazo(fecha_fin_str: str) -> Tuple[datetime, str]:
    """Intenta parsear la fecha de fin y devuelve (datetime, texto_dias_restantes)."""
    if not fecha_fin_str:
        return None, ""
    
    # Formatos comunes: YYYY-MM-DD o DD/MM/YYYY o DD-MM-YYYY
    m_iso = re.search(r"(\d{4})-(\d{2})-(\d{2})", fecha_fin_str)
    if m_iso:
        y, mo, d = map(int, m_iso.groups())
        dt = datetime(y, mo, d, 23, 59, 59)
    else:
        m_es = re.search(r"(\d{2})[/-](\d{2})[/-](\d{4})", fecha_fin_str)
        if m_es:
            d, mo, y = map(int, m_es.groups())
            dt = datetime(y, mo, d, 23, 59, 59)
        else:
            return None, ""

    hoy = date.today()
    diff = (dt.date() - hoy).days
    if diff > 1:
        txt_dias = f" *(⏳ Quedan {diff} días)*"
    elif diff == 1:
        txt_dias = " *(⚠️ ¡Queda solo 1 día!)*"
    elif diff == 0:
        txt_dias = " *(🚨 ¡ÚLTIMO DÍA HOY!)*"
    else:
        txt_dias = " *(Convocatoria abierta / Ver bases)*"

    return dt, txt_dias

def generar_calendar_ayuda(ayuda: Dict, dt_fin: datetime) -> str:
    """Genera enlace de 1 clic a Google Calendar para fecha límite de presentación."""
    if not dt_fin:
        dt_fin = datetime.now() + timedelta(days=15, hours=14)
    start_dt = dt_fin - timedelta(hours=2)
    fmt = "%Y%m%dT%H%M%SZ"
    dates_param = f"{start_dt.strftime(fmt)}/{dt_fin.strftime(fmt)}"
    
    t_enc = urllib.parse.quote_plus(f"⏰ Fin Plazo Ayuda: {ayuda['titulo'][:40]}")
    desc = f"Subvención Pública: {ayuda['organismo']}\nPresupuesto: {ayuda['presupuesto_formato']}\n👉 Tramitar: {ayuda['sede_electronica']}"
    d_enc = urllib.parse.quote_plus(desc)
    loc_enc = urllib.parse.quote_plus("Sede Electrónica Oficial")
    
    return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={t_enc}&dates={dates_param}&details={d_enc}&location={loc_enc}"

def formatear_post_ayuda_vip(ayuda: Dict) -> str:
    """Mensaje completo con enlace a sede electrónica y bases oficiales para miembros VIP."""
    dt_fin, txt_dias = parsear_fecha_plazo(ayuda.get('fecha_fin', ''))
    url_calendar = generar_calendar_ayuda(ayuda, dt_fin)

    texto = (
        "💰 *NUEVA SUBVENCIÓN A FONDO PERDIDO DETECTADA*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📋 *Convocatoria:* {ayuda['titulo']}\n"
        f"🏛️ *Organismo:* {ayuda['organismo']}\n"
        f"💶 *Presupuesto asignado:* *{ayuda['presupuesto_formato']}*\n"
        f"👥 *Beneficiarios:* {ayuda['beneficiarios']}\n"
        f"⏳ *Plazo de solicitud hasta:* `{ayuda['fecha_fin']}`{txt_dias}\n"
        f"⏰ [Guardar Límite en Google Calendar (Aviso previo)]({url_calendar})\n\n"
        f"📝 *Resumen y finalidad:*\n_{ayuda['descripcion_finalidad']}_\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [Acceder a la Sede Electrónica Oficial para Solicitar]({ayuda['sede_electronica']})\n"
    )
    if ayuda.get("url_bases"):
        texto += f"📑 [Descargar Bases Reguladoras Oficiales]({ayuda['url_bases']})\n\n"
    texto += "⭐ _Alerta exclusiva de RadarAlertas VIP_"
    return texto

def formatear_post_ayuda_gratuito(ayuda: Dict) -> str:
    """Mensaje anzuelo para canal público o redes."""
    return (
        "🚨 *ALERTA: NUEVA AYUDA A FONDO PERDIDO*\n\n"
        f"💶 *Partida:* {ayuda['presupuesto_formato']}\n"
        f"🏛️ *Organismo:* {ayuda['organismo']}\n"
        f"👥 *Perfil:* {ayuda['beneficiarios']}\n\n"
        "🔒 *El enlace directo al trámite y los requisitos completos* están disponibles en el canal VIP.\n\n"
        "👉 [Toca aquí para abrir el Bot y desbloquear](https://t.me/RadarAletasSubastas_bot) todos los expedientes oficiales."
    )
