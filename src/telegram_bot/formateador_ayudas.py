"""
Formateador de Alertas de Ayudas y Subvenciones Públicas
Genera los mensajes ejecutivos para el canal de Telegram (VIP y Free).
"""
from typing import Dict

def formatear_post_ayuda_vip(ayuda: Dict) -> str:
    """Mensaje completo con enlace a sede electrónica y bases oficiales para miembros VIP."""
    texto = (
        "💰 *NUEVA SUBVENCIÓN A FONDO PERDIDO DETECTADA*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📋 *Convocatoria:* {ayuda['titulo']}\n"
        f"🏛️ *Organismo:* {ayuda['organismo']}\n"
        f"💶 *Presupuesto asignado:* *{ayuda['presupuesto_formato']}*\n"
        f"👥 *Beneficiarios:* {ayuda['beneficiarios']}\n"
        f"⏳ *Plazo de solicitud hasta:* `{ayuda['fecha_fin']}`\n\n"
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
        "👉 Entra en @RadarAletasSubastas_bot para desbloquear todos los expedientes oficiales."
    )
