import os
import sqlite3
import urllib.request
import json
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path("C:/Ideas/radar-alertas")
load_dotenv(BASE_DIR / ".env")

DB_PATH = BASE_DIR / "data" / "radar_usuarios.db"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_FREE_CHANNEL_ID", "-1004345947331")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID", "5674459275")

print("==================================================")
print("📊 INFORME DE MÉTRICAS ACTUALES DE RADARALERTAS")
print("==================================================")

# 1. Base de datos SQLite local
if DB_PATH.exists():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM usuarios")
    total_users = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as guias FROM usuarios WHERE descargo_guia = 1")
    total_guias = cursor.fetchone()["guias"]
    
    cursor.execute("SELECT COUNT(*) as vips FROM usuarios WHERE plan = 'vip' OR suscripcion_activa = 1")
    total_vips = cursor.fetchone()["vips"]
    
    cursor.execute("SELECT user_id, username, first_name, plan, descargo_guia, fecha_alta FROM usuarios ORDER BY rowid DESC LIMIT 10")
    recent_users = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) as alertas FROM alertas_enviadas")
    total_alertas = cursor.fetchone()["alertas"]
    
    print(f"👥 Usuarios registrados en BD: {total_users}")
    print(f"📖 Guías PDF descargadas: {total_guias}")
    print(f"⭐ Suscriptores VIP activos: {total_vips}")
    print(f"📬 Total alertas históricas en BD: {total_alertas}")
    print("\nÚltimos usuarios en BD:")
    for u in recent_users:
        print(f"  • ID: {u['user_id']} | @{u['username']} | {u['first_name']} | Plan: {u['plan']} | Guía: {u['descargo_guia']} | Alta: {u['fecha_alta']}")
else:
    print("❌ Archivo de BD no encontrado localmente.")

# 2. Consultar API en vivo de Telegram
print("\n📡 CONSULTANDO API EN VIVO DE TELEGRAM...")
if TOKEN:
    try:
        # Miembros del Canal Gratuito
        url_count = f"https://api.telegram.org/bot{TOKEN}/getChatMemberCount?chat_id={CHANNEL_ID}"
        req = urllib.request.Request(url_count)
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read().decode())
            if res.get("ok"):
                print(f"📢 Miembros en el Canal de Telegram Gratuito ({CHANNEL_ID}): {res.get('result')}")
            else:
                print(f"⚠️ Error getChatMemberCount: {res}")
    except Exception as e:
        print(f"⚠️ Error consultando canal: {e}")

    try:
        # Info del Bot
        url_me = f"https://api.telegram.org/bot{TOKEN}/getMe"
        req = urllib.request.Request(url_me)
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read().decode())
            if res.get("ok"):
                bot_user = res["result"]
                print(f"🤖 Bot Activo: @{bot_user.get('username')} ({bot_user.get('first_name')})")
    except Exception as e:
        print(f"⚠️ Error getMe: {e}")

    # Verificar ping a Render (Cloud Bot)
    try:
        url_render = "https://radar-alertas-bot.onrender.com/ping"
        req = urllib.request.Request(url_render, headers={"User-Agent": "MetricsChecker/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            res_render = json.loads(r.read().decode())
            print(f"☁️ Servidor Render: ONLINE (Versión: {res_render.get('version')}, Uptime: {res_render.get('uptime_seconds')}s)")
    except Exception as e:
        print(f"☁️ Servidor Render: {e}")
        
print("==================================================")
