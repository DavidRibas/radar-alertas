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
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ChatMemberHandler,
    filters
)

from src.telegram_bot.database import (
    inicializar_bd,
    obtener_usuarios_para_retargeting,
    marcar_retargeting_enviado
)
from src.telegram_bot.bot_alertas import (
    comando_start,
    comando_stats,
    comando_activar_manual,
    manejar_callback,
    manejar_mensaje_general,
    manejar_chat_member,
    TELEGRAM_TOKEN,
    CANAL_FREE_LINK
)

load_dotenv()

async def handle_ping(request):
    """Endpoint de salud para que la nube y UptimeRobot sepan que el servicio está activo."""
    return web.json_response({
        "status": "online",
        "service": "RadarAlertas Telegram Bot 24/7",
        "bot": "@RadarAletasSubastas_bot"
    })

async def handle_landing_page(request):
    """Sirve la Landing Page oficial en la raíz del servidor."""
    ruta_html = Path(__file__).resolve().parent.parent.parent / "docs" / "index.html"
    if not ruta_html.exists():
        ruta_html = Path(__file__).resolve().parent.parent.parent / "index.html"
    if ruta_html.exists():
        return web.Response(text=ruta_html.read_text(encoding="utf-8"), content_type="text/html")
    return web.json_response({"status": "online", "service": "RadarAlertas Landing"})

async def tarea_retargeting_periodica(app):
    """Revisa periódicamente si hay usuarios que descargaron la guía hace 24h para enviarles un seguimiento."""
    print("🔁 Motor de retargeting automático iniciado...")
    while True:
        try:
            await asyncio.sleep(1800)  # Cada 30 minutos
            pendientes = obtener_usuarios_para_retargeting()
            for u in pendientes:
                uid = u["user_id"]
                nombre = u.get("first_name", "amigo")
                msg = (
                    f"👋 ¡Hola {nombre}! ¿Qué te pareció la Guía Oficial de Subastas y Embargos del BOE?\n\n"
                    "Esperamos que te haya resultado útil para entender cómo funciona la auditoría de cargas y los depósitos oficiales.\n\n"
                    "📊 *Actualización de hoy:*\n"
                    "Nuestro radar acaba de detectar nuevas subastas de inmuebles y vehículos con más del 50% de descuento.\n\n"
                    "Si quieres recibir los expedientes completos con referencias catastrales, matrículas y enlaces judiciales directos:"
                )
                teclado = [
                    [InlineKeyboardButton("⭐ Desbloquear Canales VIP (2,99 €/mes)", callback_data="pagar_vip")],
                    [InlineKeyboardButton("📢 Ver Muestras en Canal Gratuito", url=CANAL_FREE_LINK)]
                ]
                try:
                    await app.bot.send_message(
                        chat_id=uid,
                        text=msg,
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(teclado)
                    )
                    marcar_retargeting_enviado(uid)
                    print(f"🎯 Retargeting enviado a usuario {uid} ({nombre})")
                except Exception as e:
                    print(f"No se pudo enviar retargeting a {uid}: {e}")
                    marcar_retargeting_enviado(uid)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print("Error en bucle de retargeting:", e)

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

    # Lanzar tarea de retargeting en segundo plano
    asyncio.create_task(tarea_retargeting_periodica(app))

    # 2. Servidor web HTTP para la Landing Page y keep-alive en la nube
    puerto = int(os.getenv("PORT", 8080))
    server = web.Application()
    server.router.add_get("/", handle_landing_page)
    server.router.add_get("/ping", handle_ping)
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
