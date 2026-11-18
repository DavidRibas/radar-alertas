"""
Módulo Especial Fin de Semana (Sábado 11:00 AM):
Compila las 5 mejores oportunidades de la semana (inmuebles, coches y ayudas)
para emitir un resumen exclusivo en el Canal Gratuito cuando la gente está en el móvil.
"""
import os
import sys
from pathlib import Path
import requests
from typing import Dict, List
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv()

from src.extractores.boe_inmuebles import buscar_subastas_inmuebles, filtrar_mejores_chollos
from src.extractores.boe_vehiculos import buscar_subastas_vehiculos, filtrar_mejores_vehiculos
from src.extractores.ayudas_subvenciones import obtener_convocatorias_recientes, filtrar_mejores_ayudas

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL_FREE = os.getenv("TELEGRAM_CANAL_FREE_ID", "-1004345947331")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_USER_ID", "5674459275")

def compilar_top5_semanal() -> Dict:
    """Extrae las mejores oportunidades vigentes de los últimos días."""
    print("⏳ Compilando las mejores oportunidades para el Especial Fin de Semana...")
    
    # 1. Top 2 Inmuebles
    ids_inm = buscar_subastas_inmuebles(provincia_cod="", limite=15)
    inmuebles = filtrar_mejores_chollos(ids_inm, max_resultados=2)

    # 2. Top 2 Vehículos
    ids_veh = buscar_subastas_vehiculos(limite=15)
    vehiculos = filtrar_mejores_vehiculos(ids_veh, max_resultados=2)

    # 3. Top 1 Ayuda / Subvención
    ayudas_raw = obtener_convocatorias_recientes(max_paginas=2)
    ayudas = filtrar_mejores_ayudas(ayudas_raw, max_resultados=1)

    return {
        "inmuebles": inmuebles,
        "vehiculos": vehiculos,
        "ayudas": ayudas
    }

def formatear_post_fin_de_semana(datos: Dict) -> str:
    """Genera el texto de alto valor para el Canal Gratuito."""
    lineas = []
    idx = 1

    # Inmuebles
    for inm in datos.get("inmuebles", []):
        lineas.append(
            f"*{idx}. 🏠 {inm['titulo']}*\n"
            f"   • Salida: *{inm['precio_salida_formato']}* (Tasación oficial: {inm['valor_referencia_formato']})\n"
            f"   • Ahorro estimado: *{inm['ahorro_porcentaje']}%* | Expediente: `{inm['id_subasta']}`"
        )
        idx += 1

    # Vehículos
    for veh in datos.get("vehiculos", []):
        lineas.append(
            f"*{idx}. 🚗 {veh['titulo']} ({veh['provincia']})*\n"
            f"   • Salida de puja: *{veh['precio_salida_formato']}* (Tasación: {veh['valor_referencia_formato']})\n"
            f"   • Descuento: *{veh['ahorro_porcentaje']}%* | Expediente: `{veh['id_subasta']}`"
        )
        idx += 1

    # Ayudas
    for ay in datos.get("ayudas", []):
        lineas.append(
            f"*{idx}. 💰 {ay['titulo']}*\n"
            f"   • Presupuesto: *{ay['presupuesto_total']}*\n"
            f"   • Organismo: {ay['organismo'][:40]} | BDNS: `{ay['id_convocatoria']}`"
        )
        idx += 1

    cuerpo = "\n\n".join(lineas)

    texto = (
        "🌟 *TOP 5 OPORTUNIDADES OFICIALES DEL FIN DE SEMANA* 🌟\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Si estás revisando opciones de inversión o ayudas para la semana que viene, "
        "aquí tienes la selección más destacada publicada en el BOE y la BDNS:\n\n"
        f"{cuerpo}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔒 *ACCESO VIP OFICIAL:*\n"
        "Para ver las referencias catastrales, matrículas auditadas, estado de cargas y los enlaces directos para pujar online:\n\n"
        "👉 *[Toca aquí para abrir el Bot y unirte a los Canales VIP](https://t.me/RadarAletasSubastas_bot)*"
    )
    return texto

def emitir_especial_fin_de_semana():
    """Ejecuta la compilación y publica en el canal gratuito y avisa al admin."""
    datos = compilar_top5_semanal()
    if not datos["inmuebles"] and not datos["vehiculos"]:
        print("⚠️ No hay suficientes oportunidades para el especial.")
        return

    post = formatear_post_fin_de_semana(datos)

    if CANAL_FREE and TELEGRAM_TOKEN:
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": CANAL_FREE, "text": post, "parse_mode": "Markdown"},
                timeout=20
            )
            print("📢 Especial Fin de Semana emitido en Canal Gratuito:", r.status_code)
        except Exception as e:
            print("❌ Error publicando en canal libre:", e)

    if ADMIN_ID and TELEGRAM_TOKEN:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": ADMIN_ID, "text": f"👑 *Muestra enviada a David (Especial Sábado):*\n\n{post}", "parse_mode": "Markdown"},
                timeout=20
            )
            print("📱 Notificado al admin con éxito.")
        except Exception:
            pass

if __name__ == "__main__":
    emitir_especial_fin_de_semana()
