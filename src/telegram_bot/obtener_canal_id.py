"""
Detector Automático de Canales de Telegram para RadarAlertas
Detecta todos los canales donde el bot ha sido añadido como administrador.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def detectar_todos_los_canales():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url).json()
    canales = {}
    
    for item in r.get("result", []):
        chat = None
        if "my_chat_member" in item:
            chat = item["my_chat_member"]["chat"]
        elif "channel_post" in item:
            chat = item["channel_post"]["chat"]
        
        if chat and chat.get("type") == "channel":
            cid = chat.get("id")
            title = chat.get("title")
            canales[cid] = title
            
    print("\n" + "=" * 55)
    print("📡 CANALES DE TELEGRAM DETECTADOS:")
    print("=" * 55)
    if canales:
        for cid, title in canales.items():
            print(f"✅ Canal: '{title}'  --->  ID: {cid}")
    else:
        print("⚠️ No se han detectado eventos recientes de canales.")
        print("👉 Recuerda: Crea el canal, añade a @RadarAletasSubastas_bot como admin")
        print("   y escribe un mensaje cualquiera ('hola') en el canal.")
    print("=" * 55)
    return canales

if __name__ == "__main__":
    detectar_todos_los_canales()
