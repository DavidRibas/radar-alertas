"""
Formateador de Alertas de Empleo Público y Oposiciones (BOE Sección 2B)
"""
from typing import Dict

def formatear_post_empleo_vip(em: Dict) -> str:
    """Mensaje completo para el canal VIP de Empleo Público."""
    return (
        "💼 *NUEVA CONVOCATORIA DE EMPLEO PÚBLICO*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏛️ *Organismo:* {em['organismo']}\n"
        f"📋 *Convocatoria:*\n_{em['titulo']}_\n\n"
        f"📅 *Publicado en BOE:* {em['fecha_publicacion']}\n"
        f"🆔 *Identificador:* `{em['id_convocatoria']}`\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📥 [Descargar Bases Oficiales y Plazas (PDF)]({em['url_pdf']})\n\n"
        "⭐ _Alerta exclusiva de RadarAlertas Empleo VIP_"
    )

def formatear_post_empleo_gratuito(em: Dict) -> str:
    """Mensaje teaser para redes o canal público."""
    return (
        "🚨 *NUEVAS PLAZAS DE EMPLEO PÚBLICO*\n\n"
        f"🏛️ *Organismo:* {em['organismo']}\n"
        f"📋 *Plazas:* {em['titulo'][:120]}...\n\n"
        "🔒 *Bases completas, requisitos y plazos de inscripción* en el canal VIP.\n"
        "👉 Entra en @RadarAletasSubastas_bot para acceder."
    )
