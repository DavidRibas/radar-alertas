"""
Módulo Radar de Urgencia (Alerta de Cierre 17:00h):
Detecta subastas de inmuebles y vehículos que cierran HOY mismo en el BOE
y genera una alerta de alto FOMO para el Canal Gratuito y Canales VIP.
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

from src.extractores.boe_inmuebles import buscar_subastas_inmuebles, obtener_detalle_subasta
from src.extractores.boe_vehiculos import buscar_subastas_vehiculos, obtener_detalle_vehiculo

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL_FREE = os.getenv("TELEGRAM_CANAL_FREE_ID", "-1004345947331")
CANAL_VIP = os.getenv("TELEGRAM_CANAL_VIP_ID", "-1004355179430")

def obtener_oportunidades_cierre_hoy(max_inmuebles: int = 2, max_vehiculos: int = 2) -> Dict:
    """Extrae las oportunidades que concluyen en las próximas horas."""
    # Las primeras que devuelve el portal son las más próximas a fecha fin
    ids_inm = buscar_subastas_inmuebles(provincia_cod="", limite=4)
    ids_veh = buscar_subastas_vehiculos(provincia_cod="", limite=4)

    inmuebles = []
    for i_id in ids_inm:
        det = obtener_detalle_subasta(i_id)
        if det and det.get("precio_salida", 0) > 0:
            inmuebles.append(det)
            if len(inmuebles) >= max_inmuebles:
                break

    vehiculos = []
    for v_id in ids_veh:
        vdet = obtener_detalle_vehiculo(v_id)
        if vdet and vdet.get("precio_salida", 0) > 0:
            vehiculos.append(vdet)
            if len(vehiculos) >= max_vehiculos:
                break

    return {"inmuebles": inmuebles, "vehiculos": vehiculos}

def formatear_alerta_urgencia(datos: Dict) -> str:
    """Genera el mensaje con gancho de urgencia para el canal de captación."""
    lineas = []

    for v in datos.get("vehiculos", []):
        lineas.append(
            f"🚗 *{v['titulo']}* ({v['provincia']})\n"
            f"• Salida: *{v['precio_salida_formato']}* (Tasación: {v['valor_referencia_formato']} | -{v['ahorro_porcentaje']}%)\n"
            f"• Expediente ID: `{v['id_subasta']}`"
        )

    for i in datos.get("inmuebles", []):
        lineas.append(
            f"🏠 *{i['titulo']}*\n"
            f"• Salida: *{i['precio_salida_formato']}* (Tasación: {i['valor_referencia_formato']} | -{i['ahorro_porcentaje']}%)\n"
            f"• Expediente ID: `{i['id_subasta']}`"
        )

    bloque_items = "\n\n".join(lineas)

    texto = (
        "🚨 *ÚLTIMA HORA: SUBASTAS QUE CIERRAN HOY EN EL BOE* 🚨\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "⚠️ *Atención:* Los siguientes expedientes concluyen su plazo de puja en las próximas horas.\n"
        "Una vez alcanzada la hora límite, la subasta se cerrará definitivamente:\n\n"
        f"{bloque_items}\n\n"
        "🔒 *RECUERDA:* En los Canales VIP tienes los enlaces directos a cada expediente, referencias catastrales, matrículas y dictamen de cargas completas.\n\n"
        "👉 *[Toca aquí para abrir el Bot y unirte al VIP](https://t.me/RadarAletasSubastas_bot)*"
    )
    return texto

def emitir_alerta_urgencia():
    """Ejecuta la búsqueda y emite la alerta al canal gratuito."""
    print("⏳ Ejecutando Radar de Urgencia (Cierres del día)...")
    datos = obtener_oportunidades_cierre_hoy()
    if not datos["inmuebles"] and not datos["vehiculos"]:
        print("⚠️ No hay oportunidades de cierre destacadas hoy.")
        return

    msg = formatear_alerta_urgencia(datos)
    if CANAL_FREE and TELEGRAM_TOKEN:
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": CANAL_FREE, "text": msg, "parse_mode": "Markdown"},
                timeout=15
            )
            print("📢 Alerta de Urgencia emitida en Canal Gratuito:", r.status_code)
        except Exception as e:
            print("❌ Error enviando alerta de urgencia:", e)

if __name__ == "__main__":
    emitir_alerta_urgencia()
