"""
Formateador de Alertas de Licitaciones y Contratos Públicos (BOE Sección 5A)
"""
from typing import Dict

def formatear_post_licitacion_vip(lic: Dict) -> str:
    """Mensaje completo para el canal VIP de Licitaciones."""
    return (
        "📑 *NUEVA LICITACIÓN PÚBLICA OFICIAL*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏛️ *Organismo:* {lic['organismo']}\n"
        f"📋 *Objeto del Contrato:*\n_{lic['titulo']}_\n\n"
        f"📅 *Publicado en BOE:* {lic['fecha_publicacion']}\n"
        f"🆔 *Expediente BOE:* `{lic['id_licitacion']}`\n\n"
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
        "👉 Entra en @RadarAletasSubastas_bot para desbloquearlo."
    )
