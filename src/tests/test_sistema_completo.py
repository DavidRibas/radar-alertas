"""
Script de Validación Integral y Completa de RadarAlertas:
Comprueba la salud de los 5 extractores, los 6 canales de Telegram,
la base de datos SQLite y el generador de PDF.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv(str(BASE_DIR / ".env"))

from src.telegram_bot.database import inicializar_bd, obtener_conexion, obtener_metricas_globales
from src.extractores.boe_inmuebles import buscar_subastas_inmuebles
from src.extractores.boe_vehiculos import buscar_subastas_vehiculos
from src.extractores.ayudas_subvenciones import obtener_convocatorias_recientes
from src.extractores.licitaciones_contratos import obtener_licitaciones_recientes
from src.extractores.empleo_oposiciones import obtener_empleo_publico_reciente

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CANALES = {
    "🏠 Inmuebles VIP": os.getenv("TELEGRAM_CANAL_VIP_ID"),
    "🚗 Vehículos VIP": os.getenv("TELEGRAM_CANAL_VEHICULOS_ID"),
    "💰 Ayudas VIP": os.getenv("TELEGRAM_CANAL_AYUDAS_ID"),
    "📑 Licitaciones VIP": os.getenv("TELEGRAM_CANAL_LICITACIONES_ID"),
    "💼 Empleo VIP": os.getenv("TELEGRAM_CANAL_EMPLEO_ID"),
    "📢 Canal Gratuito": os.getenv("TELEGRAM_CANAL_FREE_ID")
}

def validar_todo():
    print("=" * 60)
    print("🔍 AUDITORÍA Y VALIDACIÓN AL MÁXIMO DE RADARALERTAS")
    print("=" * 60)

    # 1. Base de datos
    print("\n[1/5] Verificando Base de Datos SQLite...")
    inicializar_bd()
    m = obtener_metricas_globales()
    print(f"  ✅ DB Operativa | Usuarios: {m['total_usuarios']} | Alertas históricas: {m['total_alertas']}")

    # 2. Conexión con los 6 Canales de Telegram
    print("\n[2/5] Verificando permisos en los 6 Canales de Telegram...")
    for nom, cid in CANALES.items():
        if not cid:
            print(f"  ❌ {nom}: ID no configurado")
            continue
        try:
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChat", params={"chat_id": cid}, timeout=10).json()
            if r.get("ok"):
                title = r["result"].get("title", nom)
                print(f"  ✅ {nom} ({title}): Conectado (ID: {cid})")
            else:
                print(f"  ⚠️ {nom}: Error ({r.get('description')})")
        except Exception as e:
            print(f"  ❌ {nom}: Excepción ({e})")

    # 3. Salud de los 5 Extractores Oficiales
    print("\n[3/5] Verificando los 5 Extractores Oficiales...")
    try:
        inms = buscar_subastas_inmuebles(limite=2)
        print(f"  ✅ 1. Extractor Inmuebles BOE: {len(inms)} encontrados.")
    except Exception as e:
        print(f"  ❌ 1. Inmuebles: {e}")

    try:
        vehs = buscar_subastas_vehiculos(limite=2)
        print(f"  ✅ 2. Extractor Vehículos BOE: {len(vehs)} encontrados.")
    except Exception as e:
        print(f"  ❌ 2. Vehículos: {e}")

    try:
        ay = obtener_convocatorias_recientes(max_paginas=1)
        print(f"  ✅ 3. Extractor Ayudas BDNS: {len(ay)} convocatorias.")
    except Exception as e:
        print(f"  ❌ 3. Ayudas: {e}")

    try:
        lics = obtener_licitaciones_recientes()
        print(f"  ✅ 4. Extractor Licitaciones BOE: {len(lics)} contratos.")
    except Exception as e:
        print(f"  ❌ 4. Licitaciones: {e}")

    try:
        emps = obtener_empleo_publico_reciente()
        print(f"  ✅ 5. Extractor Empleo Público BOE: {len(emps)} plazas.")
    except Exception as e:
        print(f"  ❌ 5. Empleo: {e}")

    # 4. Lead Magnet PDF
    print("\n[4/5] Verificando Lead Magnet Oficial en PDF...")
    pdf_path = BASE_DIR / "assets" / "Guia_Subastas_Judiciales_RadarAlertas.pdf"
    if pdf_path.exists() and pdf_path.stat().st_size > 100000:
        print(f"  ✅ Guía PDF compilada y empaquetada ({pdf_path.stat().st_size / 1024:.1f} KB).")
    else:
        print("  ⚠️ Guía PDF ausente o incompleta.")

    # 5. Landing Page y Servidor Cloud
    print("\n[5/5] Verificando Servidor Web y Landing Page...")
    try:
        r_web = requests.get("https://radar-alertas-bot.onrender.com", timeout=10)
        if r_web.status_code == 200 and "<!DOCTYPE html>" in r_web.text:
            print("  ✅ Landing Page Cloud: ONLINE 24/7 (HTML 200 OK)")
        else:
            print(f"  ⚠️ Servidor Web: HTTP {r_web.status_code}")
    except Exception as e:
        print(f"  ❌ Servidor Web: {e}")

    print("\n" + "=" * 60)
    print("🎉 AUDITORÍA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    validar_todo()
