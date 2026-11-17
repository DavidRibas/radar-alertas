"""
Bot de Telegram oficial para RadarAlertas:
- Gestión de usuarios y altas
- Pasarela de suscripción mensual al Canal VIP
- Emisión de enlaces de invitación únicos e intransferibles
- Publicación de alertas automáticas
"""
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    PreCheckoutQueryHandler
)

from src.telegram_bot.database import (
    inicializar_bd,
    registrar_o_actualizar_usuario,
    activar_suscripcion_vip,
    obtener_estado_usuario
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TU_TOKEN_AQUI")
CANAL_VIP_ID = os.getenv("TELEGRAM_CANAL_VIP_ID", "@canal_vip_demo")
CANAL_FREE_ID = os.getenv("TELEGRAM_CANAL_FREE_ID", "@canal_free_demo")

async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /start con menú interactivo de botones."""
    user = update.effective_user
    registrar_o_actualizar_usuario(user.id, user.username, user.first_name)

    estado = obtener_estado_usuario(user.id)
    es_vip = estado and estado.get("suscripcion_activa") == 1

    mensaje = (
        f"👋 ¡Hola {user.first_name}! Bienvenido a *RadarAlertas*.\n\n"
        "Monitorizamos cada día el *Boletín Oficial del Estado (BOE)* con algoritmos que detectan:\n"
        "🏠 Subastas judiciales con más del 50% de ahorro.\n"
        "⚖️ Verificación previa de cargas hipotecarias.\n"
        "📊 Cruce con precios de venta reales de mercado.\n\n"
    )

    if es_vip:
        mensaje += f"⭐ *Tu estado:* MIEMBRO VIP ACTIVO (Hasta: {estado.get('fecha_fin_suscripcion')[:10]})\n"
        teclado = [
            [InlineKeyboardButton("✈️ Ir al Canal VIP Privado", url="https://t.me/c/radar_vip_enlace")],
            [InlineKeyboardButton("📊 Consultar Mi Suscripción", callback_data="mi_estado")]
        ]
    else:
        mensaje += (
            "🔒 *Acceso exclusivo:* Suscríbete para recibir todas las alertas completas "
            "con direcciones exactas, referencias catastrales y enlaces oficiales al expediente."
        )
        teclado = [
            [InlineKeyboardButton("⭐ Desbloquear Canal VIP (14,99 €/mes)", callback_data="pagar_vip")],
            [InlineKeyboardButton("ℹ️ ¿Cómo funciona el servicio?", callback_data="info_servicio")],
            [InlineKeyboardButton("📊 Mi Cuenta", callback_data="mi_estado")]
        ]

    reply_markup = InlineKeyboardMarkup(teclado)
    await update.message.reply_text(mensaje, parse_mode="Markdown", reply_markup=reply_markup)

async def manejar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestiona los clics en los botones interactivos."""
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user

    if data == "pagar_vip":
        texto = (
            "🚀 *Pase Mensual RadarAlertas VIP*\n\n"
            "Con tu suscripción mensual obtienes:\n"
            "• Alertas inmediatas de subastas judiciales en tu móvil.\n"
            "• Enlaces directos a los expedientes oficiales del BOE.\n"
            "• Datos catastrales y cruce de precios con el mercado.\n"
            "• Sin permanencia: cancela con 1 clic cuando quieras.\n\n"
            "💳 *Precio:* 14,99 € / mes (Facturación recurrente segura vía Stripe)"
        )
        teclado = [
            [InlineKeyboardButton("💳 Pagar 14,99 € (Stripe Checkout Seguro)", url="https://buy.stripe.com/test_demo_enlace")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "mi_estado":
        estado = obtener_estado_usuario(user.id)
        if estado and estado.get("suscripcion_activa") == 1:
            texto = (
                f"✅ *Estado:* Suscripción VIP Activa\n"
                f"📅 *Válida hasta:* {estado.get('fecha_fin_suscripcion')[:10]}\n"
                f"💎 *Plan:* {estado.get('plan')}"
            )
        else:
            texto = (
                "❌ *Estado:* Cuenta Gratuita\n\n"
                "Aún no tienes activado el pase al Canal VIP.\n"
                "Para desbloquear los expedientes completos y enlaces del BOE, activa tu suscripción."
            )
        teclado = [[InlineKeyboardButton("⭐ Activar Pase VIP", callback_data="pagar_vip")]]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "info_servicio":
        texto = (
            "ℹ️ *¿Cómo funciona RadarAlertas?*\n\n"
            "1. Nuestros servidores analizan cada mañana las nuevas convocatorias del BOE.\n"
            "2. Filtramos únicamente los inmuebles y vehículos con expedientes atractivos.\n"
            "3. En cuanto se detecta una oportunidad, se publica en el Canal VIP con la ficha técnica completa.\n"
            "4. Si te interesa el inmueble, utilizas el enlace directo para inscribirte y pujar en el portal judicial."
        )
        teclado = [[InlineKeyboardButton("🔙 Volver", callback_data="volver_inicio")]]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "volver_inicio":
        teclado = [
            [InlineKeyboardButton("⭐ Desbloquear Canal VIP (14,99 €/mes)", callback_data="pagar_vip")],
            [InlineKeyboardButton("ℹ️ ¿Cómo funciona?", callback_data="info_servicio")],
            [InlineKeyboardButton("📊 Mi Cuenta", callback_data="mi_estado")]
        ]
        await query.edit_message_text("Selecciona una opción del menú:", reply_markup=InlineKeyboardMarkup(teclado))

async def comando_activar_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando de administrador para activar VIP de prueba a un usuario: /activar <user_id>"""
    if not context.args:
        await update.message.reply_text("Uso: /activar <user_id>")
        return
    try:
        target_id = int(context.args[0])
        activar_suscripcion_vip(target_id, plan="admin_test", dias=30)
        await update.message.reply_text(f"✅ Usuario {target_id} activado como VIP por 30 días.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    inicializar_bd()
    if TELEGRAM_TOKEN == "TU_TOKEN_AQUI":
        print("⚠️ AVISO: Configura TELEGRAM_BOT_TOKEN en tu archivo .env para conectar con Telegram.")
        print("👉 Para crear tu bot gratis: Abre Telegram, busca @BotFather, escribe /newbot y copia el token.")
        return

    print("🤖 Iniciando Bot de Telegram RadarAlertas...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", comando_start))
    app.add_handler(CommandHandler("activar", comando_activar_manual))
    app.add_handler(CallbackQueryHandler(manejar_callback))

    app.run_polling()

if __name__ == "__main__":
    main()
