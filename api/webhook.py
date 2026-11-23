import json
import urllib.request
from http.server import BaseHTTPRequestHandler

TELEGRAM_TOKEN = "8726470516:AAEcZxeV0S--3klJ9pmJcIcKPf4cksM3EIM"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{TELEGRAM_API}/sendMessage",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.read()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def answer_callback(callback_query_id, text=None):
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{TELEGRAM_API}/answerCallbackQuery",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.read()
    except Exception as e:
        print(f"Error answering callback: {e}")
        return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "online", "service": "RadarAlertas Webhook"}).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
        except Exception:
            update = {}

        # Manejo de mensajes de texto
        if "message" in update and "text" in update["message"]:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "").strip()

            if text.startswith("/start"):
                welcome_text = (
                    "⚡ *¡BIENVENIDO A RADARALERTAS!* ⚡\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "Monitorizamos cada madrugada el *BOE, Catastro, DGT y BDNS* "
                    "para encontrar oportunidades reales con hasta un *90% de ahorro*.\n\n"
                    "🛡️ *Cargas auditadas por IA (Art. 674 LEC)*\n"
                    "🚗 *Coches embargados DGT sin precintos*\n"
                    "🏢 *Pisos judiciales libres de ocupantes*\n\n"
                    "👇 *Elige una opción para empezar:*"
                )
                keyboard = {
                    "inline_keyboard": [
                        [
                            {"text": "🔍 Abrir Catálogo Web de Chollos", "url": "https://radar-alertas-delta.vercel.app"}
                        ],
                        [
                            {"text": "💬 Canal Oficial de WhatsApp", "url": "https://whatsapp.com/channel/0029Vb99ohpB4hdUuVdOHt2Q"}
                        ],
                        [
                            {"text": "⭐ Suscripción Mensual (14,99 €/mes)", "url": "https://buy.stripe.com/28E28s5Aq8ZBel18YRcQU03"}
                        ],
                        [
                            {"text": "🌟 Plan PRO Anual (99 €/año • Ahorra 80 €)", "url": "https://buy.stripe.com/aFa14o1kafnZccT0slcQU04"}
                        ],
                        [
                            {"text": "📢 Entrar al Canal Gratuito de Telegram", "url": "https://t.me/+JoX17328N-VkMWVk"}
                        ]
                    ]
                }
                send_message(chat_id, welcome_text, keyboard)
            else:
                resp_text = (
                    "🔎 *Consulta de Oportunidades RadarAlertas*\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "Para ver todos los expedientes activos del BOE, fotos, direcciones y la calculadora de rentabilidad, accede a nuestro portal web:\n\n"
                    "👉 https://radar-alertas-delta.vercel.app"
                )
                send_message(chat_id, resp_text)

        # Manejo de botones inline
        elif "callback_query" in update:
            cb = update["callback_query"]
            answer_callback(cb["id"], "Cargando...")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode('utf-8'))
