"""
Generador de mensajes atractivos y profesionales para Telegram (Canal VIP y Canal Gratuito).
"""

def formatear_post_vip(s: dict) -> str:
    """Genera el mensaje completo y detallado para los suscriptores de pago del Canal VIP."""
    return f"""🚨 *NUEVA SUBASTA JUDICIAL DETECTADA EN MADRID* 🚨

📍 *Inmueble:* {s.get('titulo', 'Vivienda')}
📮 *Dirección:* `{s.get('direccion', 'Madrid')}`
📑 *Catastro:* `{s.get('referencia_catastral', 'Consultar expediente')}`

💰 *Valor de Tasación / Subasta:* {s.get('valor_referencia_formato', '0 €')}
🟢 *Precio de Salida:* *{s.get('precio_salida_formato', '0 €')}*
📉 *Descuento estimado:* *{s.get('ahorro_porcentaje', 0)}%*
💵 *Fianza para pujar (BOE):* *{s.get('deposito', '5%')}* _(Depósito 5% legal reembolsable al 100% si no ganas)_

⚖️ *Dictamen de Cargas:*
✔ Expediente analizado sin cargas hipotecarias preferentes conocidas.
⏳ *Cierre de pujas:* {s.get('fecha_fin', 'Próximos días')}

🔗 *Enlace directo al expediente oficial del BOE:*
[Abrir Ficha Oficial en subastas.boe.es]({s.get('url_oficial')})

_Expediente ID: {s.get('id_subasta')} • RadarAlertas VIP_
"""

def formatear_post_gratuito(s: dict, bot_username: str = "RadarAlertasBot") -> str:
    """
    Genera el post teaser para el Canal Público Gratuito.
    Oculta los datos exactos para generar deseo de suscripción.
    """
    return f"""⚠️ *NUEVA OPORTUNIDAD EN EL BOE (MADRID)* ⚠️

📍 *Ubicación:* {s.get('localidad', 'Madrid')} (Zona {s.get('codigo_postal', 'Madrid')})
💰 *Valor Oficial:* {s.get('valor_referencia_formato', '0 €')}
🟢 *Precio de Salida:* *{s.get('precio_salida_formato', '0 €')}* (-{s.get('ahorro_porcentaje', 0)}% de ahorro)

🔒 *La dirección exacta, referencia catastral y el enlace directo al BOE están reservados para los miembros del Canal VIP.*

👉 [Toca aquí para desbloquear las alertas completas en el Bot](https://t.me/{bot_username}?start=vip)
"""
