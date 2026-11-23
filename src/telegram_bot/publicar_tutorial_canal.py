"""
Script para publicar el Vídeo Tutorial Oficial en el Canal Gratuito de Telegram
y fijarlo como mensaje destacado.
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
WHATSAPP_LINK = os.getenv("WHATSAPP_CHANNEL_LINK", "https://whatsapp.com/channel/0029Vb99ohpB4hdUuVdOHt2Q")

RUTA_VIDEO = BASE_DIR / "docs" / "assets" / "tutorial_radaralertas.mp4"
if not RUTA_VIDEO.exists():
    RUTA_VIDEO = BASE_DIR / "output" / "semana_actual" / "00_TUTORIAL_COMO_FUNCIONA_RADARALERTAS.mp4"

def publicar_tutorial():
    if not RUTA_VIDEO.exists():
        print(f"❌ Error: No se encuentra el archivo de vídeo en {RUTA_VIDEO}")
        return

    print(f"📹 Subiendo vídeo tutorial ({RUTA_VIDEO.stat().st_size / 1024:.0f} KB) al canal {CANAL_FREE_ID}...")

    caption = (
        "🎥 *¿CÓMO FUNCIONA RADARALERTAS? (VÍDEO 1 MIN)* 🍿\n\n"
        "Te explicamos en menos de 1 minuto cómo cazar oportunidades reales del BOE, DGT y BDNS sin perder horas en portales judiciales:\n\n"
        "📡 *1. Rastreo Inteligente:* Monitorizamos cada madrugada miles de boletines oficiales.\n"
        "🌐 *2. Web App Interactiva:* Filtra de inmediato por provincia y tipo de bien.\n"
        "🧮 *3. Cancelación de Cargas (Art. 674 LEC):* Te mostramos cómo adjudicarte bienes libres de deudas a 0 €.\n"
        "💬 *4. Alertas en Tiempo Real:* Avisos directos en WhatsApp y Telegram antes del cierre de pujas.\n\n"
        "👇 *PRUEBA EL BUSCADOR GRATIS O ÚNETE A LA COMUNIDAD:*"
    )

    teclado = {
        "inline_keyboard": [
            [{"text": "⚡ Probar Explorador Web (BOE/DGT) 🌐", "url": f"{WEB_URL}?ref=telegram_canal"}],
            [{"text": "🤖 Abrir el Bot de Alertas", "url": f"https://t.me/{BOT_USERNAME}"}],
            [{"text": "💬 Unirse al Canal de WhatsApp 📱", "url": WHATSAPP_LINK}]
        ]
    }

    cmd = [
        "curl.exe", "-s", "-m", "60",
        f"https://api.telegram.org/bot{TOKEN}/sendVideo",
        "-F", f"chat_id={CANAL_FREE_ID}",
        "-F", f"video=@{RUTA_VIDEO}",
        "-F", f"caption={caption}",
        "-F", "parse_mode=Markdown",
        "-F", "supports_streaming=true",
        "-F", f"reply_markup={json.dumps(teclado)}"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(res.stdout)
        if data.get("ok"):
            msg_id = data["result"]["message_id"]
            print(f"✅ Vídeo publicado con éxito! ID: {msg_id}")
            
            # Opcional: fijar el mensaje en el canal
            cmd_pin = [
                "curl.exe", "-s", "-m", "15",
                f"https://api.telegram.org/bot{TOKEN}/pinChatMessage",
                "-d", f"chat_id={CANAL_FREE_ID}",
                "-d", f"message_id={msg_id}"
            ]
            res_pin = subprocess.run(cmd_pin, capture_output=True, text=True)
            print("📌 Mensaje fijado en el canal:", res_pin.stdout)
        else:
            print("❌ Error de Telegram:", data)
    except Exception as e:
        print("❌ Error parseando respuesta:", e, res.stdout)

if __name__ == "__main__":
    publicar_tutorial()
