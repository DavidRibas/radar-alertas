"""
Formateador de alertas de vehículos y coches embargados para Telegram:
Genera fichas técnicas para el Canal VIP y teasers con gancho para el Canal Gratuito.
"""
from typing import Dict

def formatear_post_vehiculo_vip(v: Dict) -> str:
    """Formatea la ficha completa del vehículo para el canal VIP privado."""
    cargas = v.get("cargas", "No constan cargas preferentes.")
    if not cargas or len(cargas) < 5:
        cargas = "Sin cargas preferentes conocidas en el expediente."

    score_txt = v.get("score_badge", "⭐ 8.5/10 (Oportunidad Oro 🏆)")
    url_maps = v.get("url_maps", "")
    url_coches = v.get("url_coches_net", "")
    url_calendar = v.get("url_calendar", "")

    linea_deposito = f"🏢 *Depósito:* `{v['deposito_lugar']}`"
    if url_maps:
        linea_deposito += f" • [📍 Ver en Google Maps]({url_maps})"

    linea_mercado = ""
    if url_coches:
        linea_mercado += f"🏷️ [Comparar Precios en Coches.net]({url_coches})\n"
    if url_calendar:
        linea_mercado += f"⏰ [Guardar en mi Google Calendar (Aviso 2h antes)]({url_calendar})\n"

    texto = (
        "🚗 *NUEVO VEHÍCULO EN SUBASTA PÚBLICA DETECTADO* 🚗\n\n"
        f"{score_txt}\n\n"
        f"🚙 *Modelo:* {v['titulo']}\n"
        f"📍 *Provincia:* {v['provincia']}\n"
        f"{linea_deposito}\n"
        f"{linea_mercado}"
        f"🏷️ *Matrícula:* `{v['matricula']}`\n"
        f"🔢 *Bastidor:* `{v['bastidor']}`\n"
        f"📅 *Año Matriculación:* {v['fecha_matriculacion']}\n"
        f"👁️ *Inspección mecánica / Visitable:* {v['visitable']}\n\n"
        f"💰 *Valor de Tasación:* {v['valor_referencia_formato']}\n"
        f"🟢 *Precio de Salida:* {v['precio_salida_formato']}\n"
        f"📉 *Descuento estimado:* {v['ahorro_porcentaje']}%\n"
        f"💵 *Fianza para pujar (BOE):* *{v['deposito']}* _(Depósito 5% oficial reembolsable si no ganas)_\n\n"
        "⚖️ *Dictamen de Cargas y Estado:*\n"
        f"✔️ {cargas}\n"
        f"⏳ *Cierre de pujas:* {v['fecha_fin']}\n\n"
        "🔗 *Enlace directo al expediente oficial del BOE:*\n"
        f"[Abrir Ficha Oficial y Pujar en subastas.boe.es]({v['url_oficial']})\n\n"
        f"_Expediente ID: {v['id_subasta']} • RadarAlertas VIP_"
    )
    return texto

def formatear_post_vehiculo_gratuito(v: Dict) -> str:
    """Formatea el post teaser para el canal gratuito de captación."""
    score_txt = v.get("score_badge", "⭐ 8.5/10 (Oportunidad Oro 🏆)")
    texto = (
        "🚗 *OPORTUNIDAD EN VEHÍCULOS DETECTADA (BOE)* 🚗\n\n"
        f"{score_txt}\n\n"
        f"🚙 *Modelo:* {v['titulo']}\n"
        f"📍 *Zona:* {v['provincia']}\n"
        f"💰 *Tasación Oficial:* {v['valor_referencia_formato']}\n"
        f"🟢 *Salida de Subasta:* {v['precio_salida_formato']}\n"
        f"🔥 *Ahorro Estimado:* -{v['ahorro_porcentaje']}%\n"
        f"💵 *Fianza:* {v['deposito']} (reembolsable)\n\n"
        "🔒 *DATOS PROTEGIDOS PARA MIEMBROS VIP:*\n"
        "• Matrícula completa y número de bastidor auditado.\n"
        "• Ubicación exacta con enlace directo a Google Maps para revisarlo en persona.\n"
        "• Comprobación de multas, precintos o cargas pendientes.\n"
        "• Enlace directo a la puja oficial en el portal del BOE.\n\n"
        "👉 *[Toca aquí para abrir el Bot y entrar al Canal VIP](https://t.me/RadarAletasSubastas_bot)*"
    )
    return texto
