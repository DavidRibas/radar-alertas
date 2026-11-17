"""
Script de utilidad para detectar automáticamente el ID numérico de tu Canal VIP de Telegram.
"""
import asyncio
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def obtener_canal_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url).json()
    print("Buscando eventos recientes del bot...")
    for item in r.get("result", []):
        # Si fue añadido a un canal
        if "my_chat_member" in item:
            chat = item["my_chat_member"]["chat"]
            print(f"🎯 ¡Canal detectado!: '{chat.get('title')}' con ID: {chat.get('id')}")
            return chat.get("id")
        if "channel_post" in item:
            chat = item["channel_post"]["chat"]
            print(f"🎯 ¡Canal detectado por mensaje!: '{chat.get('title')}' con ID: {chat.get('id')}")
            return chat.get("id")
    print("Aún no se ha detectado el canal. Escribe cualquier mensaje de prueba en el canal para que el bot lo lea.")
    return None

if __name__ == "__main__":
    obtener_canal_id()
