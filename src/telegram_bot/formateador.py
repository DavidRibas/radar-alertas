"""
Generador de mensajes atractivos y profesionales para Telegram (Canal VIP y Canal Gratuito).
"""

def formatear_post_vip(s: dict) -> str:
    """Genera el mensaje completo y detallado para los suscriptores de pago del Canal VIP."""
    score_txt = s.get('score_badge', '⭐ 8.5/10 (Oportunidad Oro 🏆)')
    sit_pos = s.get('situacion_posesoria', '⚪ No especificada en edicto')
    visitable = s.get('visitable', 'No consta')
    url_maps = s.get('url_maps', '')
    url_catastro = s.get('url_catastro')

    linea_catastro = f"📑 *Catastro:* `{s.get('referencia_catastral', 'Consultar expediente')}`"
    if url_catastro:
        linea_catastro += f" • [Ver Ficha y Metros en Catastro]({url_catastro})"

    linea_maps = ""
    if url_maps:
        linea_maps = f"📍 [Ver Fachada y Entorno en Google Street View]({url_maps})\n"

    return f"""🚨 *NUEVA SUBASTA JUDICIAL DETECTADA EN MADRID* 🚨

{score_txt}

📍 *Inmueble:* {s.get('titulo', 'Vivienda')}
📮 *Dirección:* `{s.get('direccion', 'Madrid')}`
{linea_maps}{linea_catastro}

💰 *Valor de Tasación Oficial:* {s.get('valor_referencia_formato', '0 €')}
🟢 *Precio de Salida:* *{s.get('precio_salida_formato', '0 €')}*
📉 *Descuento estimado:* *{s.get('ahorro_porcentaje', 0)}%*
💵 *Fianza para pujar (BOE):* *{s.get('deposito', '5%')}* _(Depósito 5% oficial reembolsable al 100% si no ganas)_

🔍 *AUDITORÍA JUDICIAL Y OCUPACIÓN:*
• *Estado Posesorio:* {sit_pos}
• *Inspección / Visitable:* {visitable}
• *Dictamen de Cargas:* ✔ Cargas anteriores canceladas por decreto judicial (Art. 674 LEC).
⏳ *Cierre de pujas:* {s.get('fecha_fin', 'Próximos días')}

🔗 *Enlace directo al portal oficial de subastas:*
👉 [Abrir Ficha Oficial y Pujar en subastas.boe.es]({s.get('url_oficial')})

_Expediente ID: {s.get('id_subasta')} • RadarAlertas VIP_
"""

def formatear_post_gratuito(s: dict, bot_username: str = "RadarAlertasBot") -> str:
    """
    Genera el post teaser para el Canal Público Gratuito.
    Oculta los datos exactos para generar deseo de suscripción.
    """
    score_txt = s.get('score_badge', '⭐ 8.5/10 (Oportunidad Oro 🏆)')
    return f"""⚠️ *NUEVA OPORTUNIDAD EN EL BOE (MADRID)* ⚠️

{score_txt}

📍 *Ubicación:* {s.get('localidad', 'Madrid')} (Zona {s.get('codigo_postal', 'Madrid')})
💰 *Valor Oficial:* {s.get('valor_referencia_formato', '0 €')}
🟢 *Precio de Salida:* *{s.get('precio_salida_formato', '0 €')}* (-{s.get('ahorro_porcentaje', 0)}% de ahorro)
💵 *Fianza requerida:* {s.get('deposito', '5%')} (reembolsable)

🔒 *DATOS PROTEGIDOS PARA MIEMBROS VIP:*
• Dirección exacta con enlace directo a Google Street View.
• Estado de ocupación auditado (libre vs ocupado).
• Ficha catastral oficial con metros cuadrados y planos.
• Enlace judicial directo al BOE para pujar.

👉 [Toca aquí para desbloquear las alertas completas en el Bot](https://t.me/{bot_username}?start=vip)
"""
