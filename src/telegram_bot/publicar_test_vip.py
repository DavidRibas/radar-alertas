import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(BASE_ROOT) not in sys.path:
    sys.path.insert(0, str(BASE_ROOT))

from src.extractores.boe_inmuebles import buscar_subastas_inmuebles, filtrar_mejores_chollos
from src.telegram_bot.formateador import formatear_post_vip

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL_ID = os.getenv("TELEGRAM_CANAL_VIP_ID")

def enviar_alerta_test():
    print("🔍 Obteniendo la mejor subasta judicial activa del BOE...")
    ids = buscar_subastas_inmuebles("28", limite=15)
    mejores = filtrar_mejores_chollos(ids, max_resultados=1)
    
    if not mejores:
        print("No se encontraron subastas con filtros hoy.")
        return

    chollo = mejores[0]
    mensaje = formatear_post_vip(chollo)

    print(f"📤 Enviando alerta al canal VIP ({CANAL_ID})...")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CANAL_ID,
        "text": mensaje,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    r = requests.post(url, json=payload).json()
    if r.get("ok"):
        print("🎉 ¡ALERTA PUBLICADA CON ÉXITO EN EL CANAL PRIVADO!")
    else:
        print(f"❌ Error al publicar: {r}")

if __name__ == "__main__":
    enviar_alerta_test()
