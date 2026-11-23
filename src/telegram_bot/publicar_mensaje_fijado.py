"""
Publica y fija el Mensaje Oficial de Bienvenida y Recursos en el Canal Gratuito de Telegram.
Incluye enlaces directos al bot para descargar la Guía PDF, el bucle de referidos y el acceso VIP.
"""
import os
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(str(BASE_DIR / ".env"))

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CANAL_FREE_ID = os.getenv("TELEGRAM_CANAL_FREE_ID", "-1004345947331")
BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "RadarAletasSubastas_bot")
WEB_URL = "https://radar-alertas-delta.vercel.app"
WHATSAPP_CHANNEL_LINK = "https://whatsapp.com/channel/0029Vb99ohpB4hdUuVdOHt2Q"

def publicar_y_fijar_bienvenida():
    print(f"🚀 Publicando mensaje fijado de bienvenida en canal: {CANAL_FREE_ID}...")

    texto = (
        "📌 *BIENVENIDO A RADARALERTAS | TU RADAR DE OPORTUNIDADES OFICIALES* 🇪🇸\n\n"
        "Analizamos cada mañana los boletines del Estado con algoritmos inteligentes "
        "para detectar chollos reales y oportunidades antes que nadie:\n\n"
        "🏠 *Subastas Inmobiliarias:* Pisos, locales y chalets con más del 50% de descuento y cargas auditadas (Art. 674 LEC).\n"
        "🚗 *Vehículos Embargados:* Coches, furgonetas y motos en depósitos públicos desde 500 €.\n"
        "💰 *Ayudas y Subvenciones:* Dinero a fondo perdido del BDNS para autónomos, pymes y particulares.\n"
        "📑 *Licitaciones Públicas:* Contratos menores de obras y servicios para profesionales sin intermediarios.\n"
        "💼 *Empleo Público:* Plazas oficiales y bolsas urgentes publicadas en el BOE.\n\n"
        "📢 *En este canal gratuito compartimos muestras, análisis y alertas de urgencia.*\n\n"
        "👇 *RECURSOS OFICIALES Y HERRAMIENTAS GRATUITAS:* 👇"
    )

    teclado = {
        "inline_keyboard": [
            [
                {"text": "🤖 Abrir el Bot de RadarAlertas", "url": f"https://t.me/{BOT_USERNAME}"}
            ],
            [
                {"text": "🎁 Guías Gratis en PDF", "url": f"https://t.me/{BOT_USERNAME}?start=guia_gratis"},
                {"text": "🔍 Chollos por Provincia", "url": f"https://t.me/{BOT_USERNAME}?start=provincias"}
            ],
            [
                {"text": "👥 Ganar Mes VIP Gratis", "url": f"https://t.me/{BOT_USERNAME}?start=ref_invitar"},
                {"text": "⭐ Canales VIP", "url": f"https://t.me/{BOT_USERNAME}?start=vip"}
            ],
            [
                {"text": "💬 Canal Oficial de WhatsApp", "url": WHATSAPP_CHANNEL_LINK}
            ],
            [
                {"text": "🌐 Web Oficial de RadarAlertas", "url": WEB_URL}
            ]
        ]
    }

    # 1. Enviar mensaje
    payload = {
        "chat_id": CANAL_FREE_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(teclado)
    }

    cmd_send = [
        "curl.exe", "-s", "-m", "15",
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        "-d", f"chat_id={payload['chat_id']}",
        "--data-urlencode", f"text={payload['text']}",
        "-d", f"parse_mode={payload['parse_mode']}",
        "-d", f"reply_markup={payload['reply_markup']}"
    ]

    res = subprocess.run(cmd_send, capture_output=True, text=True)
    try:
        data = json.loads(res.stdout)
        if not data.get("ok"):
            print("❌ Error al enviar mensaje:", data)
            return False

        msg_id = data["result"]["message_id"]
        print(f"✅ Mensaje de bienvenida publicado con éxito (Message ID: {msg_id})")

        # 2. Fijar mensaje arriba en el canal (pinChatMessage)
        cmd_pin = [
            "curl.exe", "-s", "-m", "15",
            f"https://api.telegram.org/bot{TOKEN}/pinChatMessage",
            "-d", f"chat_id={CANAL_FREE_ID}",
            "-d", f"message_id={msg_id}"
        ]
        res_pin = subprocess.run(cmd_pin, capture_output=True, text=True)
        data_pin = json.loads(res_pin.stdout)
        if data_pin.get("ok"):
            print("📌 ¡Mensaje fijado con chincheta en el Canal Gratuito con éxito!")
            return True
        else:
            print("⚠️ No se pudo fijar con chincheta (revisar permisos de admin):", data_pin)
            return False
    except Exception as e:
        print("❌ Error parseando respuesta de Telegram:", e, res.stdout)
        return False

if __name__ == "__main__":
    publicar_y_fijar_bienvenida()
