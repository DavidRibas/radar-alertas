"""
Emisor Oficial de Alertas para la Red Completa de RadarAlertas.
Publica oportunidades verificadas en tiempo real en los 4 canales VIP de Telegram:
1. RadarAlertas Subastas VIP
2. RadarAlertas Ayudas VIP
3. RadarAlertas Licitaciones VIP
4. RadarAlertas Empleo VIP
"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(BASE_ROOT) not in sys.path:
    sys.path.insert(0, str(BASE_ROOT))

from src.extractores.boe_inmuebles import buscar_subastas_inmuebles, filtrar_mejores_chollos
from src.extractores.ayudas_subvenciones import obtener_convocatorias_recientes, filtrar_mejores_ayudas
from src.extractores.licitaciones_contratos import obtener_licitaciones_recientes
from src.extractores.empleo_oposiciones import obtener_empleo_publico_reciente

from src.telegram_bot.formateador import formatear_post_vip as formatear_subasta
from src.telegram_bot.formateador_ayudas import formatear_post_ayuda_vip
from src.telegram_bot.formateador_licitaciones import formatear_post_licitacion_vip
from src.telegram_bot.formateador_empleo import formatear_post_empleo_vip

load_dotenv(BASE_ROOT / ".env")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CANALES = {
    "subastas": {
        "id": os.getenv("TELEGRAM_CANAL_VIP_ID", "-1004355179430"),
        "nombre": "RadarAlertas Subastas VIP"
    },
    "ayudas": {
        "id": os.getenv("TELEGRAM_CANAL_AYUDAS_ID", "-1004437054989"),
        "nombre": "RadarAlertas Ayudas VIP"
    },
    "licitaciones": {
        "id": os.getenv("TELEGRAM_CANAL_LICITACIONES_ID", "-1004308901950"),
        "nombre": "RadarAlertas Licitaciones VIP"
    },
    "empleo": {
        "id": os.getenv("TELEGRAM_CANAL_EMPLEO_ID", "-1004292956298"),
        "nombre": "RadarAlertas Empleo VIP"
    }
}

def enviar_mensaje(chat_id: str, texto: str) -> bool:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    r = requests.post(url, json=payload).json()
    return r.get("ok", False)

def emitir_alerta_subastas():
    print(f"\n📡 [1/4] Obteniendo subastas judiciales...")
    subastas_raw = buscar_subastas_inmuebles("28", limite=10)
    mejores = filtrar_mejores_chollos(subastas_raw, max_resultados=1)
    if mejores:
        msg = formatear_subasta(mejores[0])
        cid = CANALES["subastas"]["id"]
        ok = enviar_mensaje(cid, msg)
        print(f"  {'✅' if ok else '❌'} Subastas -> {CANALES['subastas']['nombre']} ({cid})")
    else:
        print("  ⚠️ No se encontraron subastas con filtros hoy.")

def emitir_alerta_ayudas():
    print(f"\n📡 [2/4] Obteniendo ayudas y subvenciones (BDNS)...")
    convs = obtener_convocatorias_recientes(max_paginas=1)
    mejores = filtrar_mejores_ayudas(convs, max_resultados=1)
    if mejores:
        msg = formatear_post_ayuda_vip(mejores[0])
        cid = CANALES["ayudas"]["id"]
        ok = enviar_mensaje(cid, msg)
        print(f"  {'✅' if ok else '❌'} Ayudas -> {CANALES['ayudas']['nombre']} ({cid})")
    else:
        print("  ⚠️ No se encontraron ayudas a fondo perdido hoy.")

def emitir_alerta_licitaciones():
    print(f"\n📡 [3/4] Obteniendo licitaciones públicas (BOE 5A)...")
    lics = obtener_licitaciones_recientes()
    if lics:
        msg = formatear_post_licitacion_vip(lics[0])
        cid = CANALES["licitaciones"]["id"]
        ok = enviar_mensaje(cid, msg)
        print(f"  {'✅' if ok else '❌'} Licitaciones -> {CANALES['licitaciones']['nombre']} ({cid})")
    else:
        print("  ⚠️ No se encontraron licitaciones recientes.")

def emitir_alerta_empleo():
    print(f"\n📡 [4/4] Obteniendo empleo público y oposiciones (BOE 2B)...")
    empleos = obtener_empleo_publico_reciente()
    if empleos:
        msg = formatear_post_empleo_vip(empleos[0])
        cid = CANALES["empleo"]["id"]
        ok = enviar_mensaje(cid, msg)
        print(f"  {'✅' if ok else '❌'} Empleo -> {CANALES['empleo']['nombre']} ({cid})")
    else:
        print("  ⚠️ No se encontraron convocatorias de empleo recientes.")

def emitir_todas():
    print("=" * 60)
    print("🚀 EMISIÓN EN TIEMPO REAL: RED COMPLETA RADARALERTAS")
    print("=" * 60)
    emitir_alerta_subastas()
    emitir_alerta_ayudas()
    emitir_alerta_licitaciones()
    emitir_alerta_empleo()
    print("\n" + "=" * 60)
    print("🏁 Emisión completada en todos los canales activos.")
    print("=" * 60)

if __name__ == "__main__":
    emitir_todas()
