"""
Servicio en la Nube 24/7 para el Bot de Telegram RadarAlertas.
Incluye servidor HTTP para health-checks y compatibilidad con
plataformas PaaS (Render, Koyeb, Railway, Fly.io, etc.).
"""
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from aiohttp import web
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ChatMemberHandler,
    filters
)

from src.telegram_bot.database import inicializar_bd
from src.telegram_bot.bot_alertas import (
    comando_start,
    comando_stats,
    comando_activar_manual,
    manejar_callback,
    manejar_mensaje_general,
    manejar_chat_member,
    TELEGRAM_TOKEN
)

load_dotenv()

async def handle_ping(request):
    """Endpoint de salud para que la nube sepa que el servicio está activo."""
    return web.json_response({
        "status": "online",
        "service": "RadarAlertas Telegram Bot 24/7",
        "bot": "@RadarAletasSubastas_bot"
    })

async def main():
    inicializar_bd()

    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "TU_TOKEN_AQUI":
        print("❌ Error: TELEGRAM_BOT_TOKEN no configurado en variables de entorno.")
        return

    print("🚀 Iniciando Bot Telegram RadarAlertas en modo Nube 24/7...")

    # 1. Configurar aplicación Telegram
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", comando_start))
    app.add_handler(CommandHandler("stats", comando_stats))
    app.add_handler(CommandHandler("activar", comando_activar_manual))
    app.add_handler(CallbackQueryHandler(manejar_callback))
    app.add_handler(ChatMemberHandler(manejar_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.ALL, manejar_mensaje_general))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    print("✅ Bot de Telegram escuchando mensajes...")

    # 2. Servidor web HTTP para keep-alive en la nube
    puerto = int(os.getenv("PORT", 8080))
    server = web.Application()
    server.router.add_get("/", handle_ping)
    server.router.add_get("/healthz", handle_ping)

    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", puerto)
    await site.start()
    print(f"🌍 Servidor Web de salud activo en http://0.0.0.0:{puerto}")

    try:
        # Mantener en ejecución indefinida
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        print("Cerrando servicios...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
