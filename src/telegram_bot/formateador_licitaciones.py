"""
Formateador de Alertas de Licitaciones y Contratos Públicos (BOE Sección 5A)
"""
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict

def generar_calendar_licitacion(lic: Dict) -> str:
    """Genera recordatorio en Google Calendar para preparación de pliegos y oferta."""
    # Plazo legal estándar estimado en contratación pública: 15 días naturales
    fecha_pub_str = lic.get("fecha_publicacion", "")
    try:
        if len(fecha_pub_str) == 8:
            dt_pub = datetime.strptime(fecha_pub_str, "%Y%m%d")
        else:
            dt_pub = datetime.now()
    except Exception:
        dt_pub = datetime.now()

    dt_limite = dt_pub + timedelta(days=15, hours=14)
    start_dt = dt_limite - timedelta(hours=2)
    fmt = "%Y%m%dT%H%M%SZ"
    dates_param = f"{start_dt.strftime(fmt)}/{dt_limite.strftime(fmt)}"

    t_enc = urllib.parse.quote_plus(f"⏰ Límite Oferta: {lic['titulo'][:40]}")
    desc = f"Contrato Público Oficial BOE\nOrganismo: {lic['organismo']}\nExpediente: {lic['id_licitacion']}\n👉 Pliego PDF: {lic['url_pdf']}"
    d_enc = urllib.parse.quote_plus(desc)
    loc_enc = urllib.parse.quote_plus("Plataforma de Contratación del Sector Público")

    return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={t_enc}&dates={dates_param}&details={d_enc}&location={loc_enc}"

def formatear_post_licitacion_vip(lic: Dict) -> str:
    """Mensaje completo para el canal VIP de Licitaciones."""
    url_calendar = generar_calendar_licitacion(lic)
    return (
        "📑 *NUEVA LICITACIÓN PÚBLICA OFICIAL*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏛️ *Organismo:* {lic['organismo']}\n"
        f"📋 *Objeto del Contrato:*\n_{lic['titulo']}_\n\n"
        f"📅 *Publicado en BOE:* {lic['fecha_publicacion']}\n"
        f"🆔 *Expediente BOE:* `{lic['id_licitacion']}`\n\n"
        f"⏰ [Guardar Recordatorio Pliego en Google Calendar]({url_calendar})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📥 [Descargar Pliego Oficial y Condiciones (PDF)]({lic['url_pdf']})\n\n"
        "⭐ _Alerta exclusiva de RadarAlertas Licitaciones VIP_"
    )

def formatear_post_licitacion_gratuito(lic: Dict) -> str:
    """Mensaje teaser para redes o canal público."""
    return (
        "🚨 *NUEVO CONTRATO PÚBLICO DISPONIBLE*\n\n"
        f"🏛️ *Organismo:* {lic['organismo']}\n"
        f"📋 *Objeto:* {lic['titulo'][:120]}...\n\n"
        "🔒 *Descarga los pliegos y condiciones oficiales* en nuestro canal VIP.\n"
        "👉 [Toca aquí para abrir el Bot y desbloquear los pliegos](https://t.me/RadarAletasSubastas_bot)."
    )
