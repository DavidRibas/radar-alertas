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
    marcar_retargeting_enviado,
    activar_suscripcion_vip,
    registrar_pago_stripe,
    obtener_usuarios_para_recordatorio_renovacion,
    marcar_aviso_renovacion_enviado,
    procesar_suscripciones_vencidas,
    registrar_visita_web,
    obtener_metricas_visitas,
    ya_fue_enviada,
    registrar_alerta_enviada
)
from src.telegram_bot.bot_alertas import (
    comando_start,
    comando_stats,
    comando_activar_manual,
    comando_invitar,
    comando_auditar,
    comando_web,
    manejar_callback,
    manejar_mensaje_general,
    manejar_chat_member,
    TELEGRAM_TOKEN,
    CANAL_FREE_LINK,
    CANAL_FREE_ID,
    ADMIN_ID,
    CANAL_VIP_ID,
    CANAL_VEHICULOS_ID,
    CANAL_AYUDAS_ID,
    CANAL_LICITACIONES_ID,
    CANAL_EMPLEO_ID
)

load_dotenv()

app_instance = None

async def handle_ping(request):
    """Endpoint de salud para que la nube y UptimeRobot sepan que el servicio está activo."""
    return web.json_response({
        "status": "online",
        "service": "RadarAlertas Telegram Bot 24/7",
        "version": "v2.8-clean",
        "bot": "@RadarAletasSubastas_bot"
    })

async def handle_track_visit(request):
    """Registra una visita anónima desde la web."""
    try:
        ref = request.query.get("ref", "directo")
        pagina = request.query.get("p", "/")
        ua = request.headers.get("User-Agent", "desconocido")

        ua_lower = ua.lower()
        if "iphone" in ua_lower or "ipad" in ua_lower:
            disp = "iOS"
        elif "android" in ua_lower:
            disp = "Android"
        elif "mobile" in ua_lower:
            disp = "Móvil"
        else:
            disp = "Escritorio"

        ip = request.remote or request.headers.get("X-Forwarded-For", "anon")
        import hashlib
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16]

        registrar_visita_web(origen=ref, pagina=pagina, dispositivo=disp, user_agent=ua, ip_hash=ip_hash)
    except Exception as e:
        print(f"Error registrando visita: {e}")

    return web.json_response(
        {"ok": True},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

async def handle_landing_page(request):
    """Sirve la Landing Page oficial en la raíz del servidor."""
    ruta_html = Path(__file__).resolve().parent.parent.parent / "docs" / "index.html"
    if not ruta_html.exists():
        ruta_html = Path(__file__).resolve().parent.parent.parent / "index.html"
    if ruta_html.exists():
        return web.Response(text=ruta_html.read_text(encoding="utf-8"), content_type="text/html")
    return web.json_response({"status": "online", "service": "RadarAlertas Landing"})

async def handle_stripe_webhook(request):
    """Procesa las notificaciones automáticas de pago de Stripe en tiempo real."""
    global app_instance
    try:
        payload = await request.json()
        event_type = payload.get("type")

        if event_type == "checkout.session.completed":
            session = payload.get("data", {}).get("object", {})
            client_ref = session.get("client_reference_id")
            customer_email = session.get("customer_details", {}).get("email") or session.get("customer_email", "desconocido")
            amount_total = session.get("amount_total", 0) / 100.0
            currency = session.get("currency", "eur").upper()
            session_id = session.get("id", "")

            # Identificar si es Pack Total (4,99 €) o Individual (2,99 €)
            es_pack_total = amount_total >= 4.0
            plan_nombre = "Pack Total VIP" if es_pack_total else "Canal VIP Individual"

            uid_int = int(client_ref) if client_ref and str(client_ref).isdigit() else None

            # 1. Registrar en Base de Datos
            registrar_pago_stripe(session_id, uid_int, customer_email, amount_total, currency, plan_nombre)

            # 2. Si tenemos el ID de Telegram del usuario, activar y entregar accesos automáticamente
            if uid_int and app_instance:
                activar_suscripcion_vip(uid_int, plan=plan_nombre, dias=30)

                botones_canales = []
                canales_a_entregar = [
                    ("🏠 Canal Subastas Inmuebles", CANAL_VIP_ID),
                    ("🚗 Canal Vehículos Embargados", CANAL_VEHICULOS_ID),
                    ("💰 Canal Ayudas y Subvenciones", CANAL_AYUDAS_ID),
                    ("📑 Canal Licitaciones Públicas", CANAL_LICITACIONES_ID),
                    ("💼 Canal Empleo y Oposiciones", CANAL_EMPLEO_ID)
                ] if es_pack_total else [("⭐ Tu Canal VIP Seleccionado", CANAL_VIP_ID)]

                for nombre_ch, cid in canales_a_entregar:
                    try:
                        inv = await app_instance.bot.create_chat_invite_link(
                            chat_id=cid,
                            member_limit=1,
                            name=f"VIP_{uid_int}"
                        )
                        botones_canales.append([InlineKeyboardButton(f"👉 Entrar a {nombre_ch}", url=inv.invite_link)])
                    except Exception as err:
                        print(f"Error generando enlace para {nombre_ch}: {err}")

                mensaje_usuario = (
                    "🎉 *¡PAGO CONFIRMADO CON ÉXITO!* 🎉\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"¡Bienvenido a *RadarAlertas VIP*! Tu suscripción ({plan_nombre}) está **activa por 30 días**.\n\n"
                    "👇 *Toca los botones para unirte a tus canales privados:*\n"
                    "_(Son enlaces exclusivos de 1 solo uso generados para ti)_"
                )
                try:
                    await app_instance.bot.send_message(
                        chat_id=uid_int,
                        text=mensaje_usuario,
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(botones_canales)
                    )
                    print(f"✅ Usuario {uid_int} activado automáticamente tras pago de {amount_total} €.")
                except Exception as e_send:
                    print(f"No se pudo enviar mensaje al usuario {uid_int}: {e_send}")

            # 3. Notificar inmediatamente al Administrador (David)
            if ADMIN_ID and app_instance:
                aviso_admin = (
                    "💰 *¡NUEVO PAGO RECIBIDO EN STRIPE!* 💰\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    f"💶 *Importe:* {amount_total:.2f} {currency}\n"
                    f"📦 *Plan:* {plan_nombre}\n"
                    f"📧 *Email Cliente:* {customer_email}\n"
                    f"🆔 *Telegram User ID:* `{client_ref or 'Directo Web'}`\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🟢 *Estado:* Activado y entregado automáticamente."
                )
                try:
                    await app_instance.bot.send_message(
                        chat_id=int(ADMIN_ID),
                        text=aviso_admin,
                        parse_mode="Markdown"
                    )
                except Exception as e_admin:
                    print(f"No se pudo avisar a admin: {e_admin}")

        return web.json_response({"status": "received", "event": event_type})
    except Exception as e:
        print(f"❌ Error en webhook Stripe: {e}")
        return web.json_response({"status": "error", "message": str(e)}, status=400)

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
                    [InlineKeyboardButton("📢 Ver Alertas en Directo (Gratis)", url=CANAL_FREE_LINK)]
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

async def tarea_renovaciones_periodica(app):
    """Revisa periódicamente si hay suscripciones VIP próximas a caducar (3 días) o recién vencidas."""
    print("🔁 Motor de renovaciones automáticas y anti-churn iniciado...")
    while True:
        try:
            await asyncio.sleep(3600)  # Cada 1 hora
            # 1. Avisar a usuarios cuyo VIP vence en menos de 72 horas
            proximos = obtener_usuarios_para_recordatorio_renovacion()
            for u in proximos:
                uid = u["user_id"]
                nombre = u.get("first_name", "amigo")
                plan = u.get("plan", "VIP")
                fecha_fin_str = str(u.get("fecha_fin_suscripcion", ""))[:10]

                msg = (
                    f"⏰ *Aviso de Renovación de Suscripción VIP*\n\n"
                    f"Hola {nombre}, te recordamos que tu suscripción *{plan}* vence el próximo *{fecha_fin_str}* (en menos de 3 días).\n\n"
                    "Para seguir recibiendo los expedientes completos del BOE, coches embargados y ayudas directas sin interrupciones, "
                    "puedes renovar con un solo clic:"
                )
                teclado = [
                    [InlineKeyboardButton("⭐ Renovar mi Suscripción VIP", callback_data="pagar_vip")],
                    [InlineKeyboardButton("👥 Ganar Mes Gratis Invitando Amigos", callback_data="menu_referidos")]
                ]
                try:
                    await app.bot.send_message(
                        chat_id=uid,
                        text=msg,
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(teclado)
                    )
                    marcar_aviso_renovacion_enviado(uid)
                    print(f"⏰ Recordatorio de renovación enviado a usuario {uid} ({nombre})")
                except Exception as e_user:
                    print(f"No se pudo enviar aviso de renovación a {uid}: {e_user}")
                    marcar_aviso_renovacion_enviado(uid)

            # 2. Gestionar suscripciones que han llegado a su fecha de vencimiento
            vencidos = procesar_suscripciones_vencidas()
            for v in vencidos:
                uid = v["user_id"]
                nombre = v.get("first_name", "amigo")
                msg_vencido = (
                    f"⚠️ *Tu Suscripción VIP ha finalizado*\n\n"
                    f"Hola {nombre}, tu acceso a los canales VIP de RadarAlertas ha expirado.\n\n"
                    "Si deseas reactivar tus alertas para no perderte los chollos y subastas de esta semana:"
                )
                teclado = [
                    [InlineKeyboardButton("⭐ Reactivar mi Pase VIP", callback_data="pagar_vip")],
                    [InlineKeyboardButton("📢 Ver Alertas en Directo (Gratis)", url=CANAL_FREE_LINK)]
                ]
                try:
                    await app.bot.send_message(
                        chat_id=uid,
                        text=msg_vencido,
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(teclado)
                    )
                    print(f"🔒 Notificación de vencimiento enviada a {uid}")
                except Exception as e_v:
                    print(f"No se pudo notificar vencimiento a {uid}: {e_v}")
        except asyncio.CancelledError:
            break
        except Exception as e:
            print("Error en bucle de renovaciones:", e)

async def tarea_publicar_chollo_diario(app):
    """Emite periódicamente el Chollo del Día en el Canal Gratuito de Telegram para fidelizar y retener."""
    print("📢 Motor autónomo de emisión diaria en Canal Gratuito iniciado...")
    await asyncio.sleep(45)  # Espera inicial tras arranque
    while True:
        try:
            ahora = datetime.now()
            ruta_cat = Path(__file__).resolve().parent.parent.parent / "docs" / "data" / "oportunidades.json"
            if not ruta_cat.exists():
                ruta_cat = Path(__file__).resolve().parent.parent.parent / "data" / "oportunidades.json"

            if ruta_cat.exists():
                with open(ruta_cat, "r", encoding="utf-8") as f:
                    catalogo = json.load(f)

                if catalogo:
                    dia_ano = ahora.timetuple().tm_yday
                    item = catalogo[dia_ano % len(catalogo)]
                    fecha_clave = ahora.strftime("%Y-%m-%d")
                    id_alerta = f"FREE-{item.get('id', 'chollo')}-{fecha_clave}"

                    if not ya_fue_enviada(id_alerta):
                        tipo = item.get("tipo", "inmueble")
                        icono = "🚗" if tipo == "vehiculo" else ("💼" if tipo == "empleo" else "🏠")
                        titulo = item.get("titulo", "Oportunidad Destacada")
                        precio_salida = item.get("precioBoe", "Consultar")
                        precio_mercado = item.get("precioMercado", "Consultar")
                        ahorro = item.get("ahorro", "Gran Descuento")
                        ubicacion = item.get("ubicacion", "España")
                        legal = item.get("legal", "0,00 € cargas previas (Art. 674 LEC)")

                        caption = (
                            f"🚨 *CHOLLO DEL DÍA AUDITADO POR EL RADAR* {icono}\n\n"
                            f"Acaba de ser auditada esta oportunidad oficial con gran descuento:\n\n"
                            f"📌 *Detalle:* {titulo}\n"
                            f"📍 *Ubicación:* {ubicacion}\n"
                            f"🏷️ *Ahorro:* *{ahorro}*\n\n"
                            f"📊 *Valor Estimado:* {precio_mercado}\n"
                            f"🎯 *Precio de Salida:* *{precio_salida}*\n"
                            f"🛡️ *Garantía:* {legal}\n\n"
                            f"👇 *Accede al expediente oficial, mapa interactivo y simulador de cargas:*"
                        )
                        teclado = [
                            [InlineKeyboardButton("⚡ Ver Ficha en el Buscador Web Oficial 🌐", url="https://radar-alertas-delta.vercel.app/?ref=telegram_chollo_auto")],
                            [InlineKeyboardButton("🧮 Simular Gastos y Tasas (Art. 674 LEC)", url="https://radar-alertas-delta.vercel.app/#calculadora")]
                        ]

                        canal_id = CANAL_FREE_ID or os.getenv("TELEGRAM_CANAL_FREE_ID", "-1004345947331")
                        img_rel = item.get("img", "")
                        img_path = Path(__file__).resolve().parent.parent.parent / "docs" / img_rel
                        if not img_path.exists():
                            img_path = Path(__file__).resolve().parent.parent.parent / img_rel

                        if img_path.exists():
                            with open(img_path, "rb") as foto:
                                await app.bot.send_photo(
                                    chat_id=canal_id,
                                    photo=foto,
                                    caption=caption,
                                    parse_mode="Markdown",
                                    reply_markup=InlineKeyboardMarkup(teclado)
                                )
                        else:
                            await app.bot.send_message(
                                chat_id=canal_id,
                                text=caption,
                                parse_mode="Markdown",
                                reply_markup=InlineKeyboardMarkup(teclado)
                            )
                        registrar_alerta_enviada(id_alerta, titulo, precio_salida)
                        print(f"✅ Chollo del día enviado automáticamente al Canal Gratuito: {titulo}")

            # Revisar cada 4 horas
            await asyncio.sleep(14400)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error en tarea_publicar_chollo_diario: {e}")
            await asyncio.sleep(3600)

async def main():
    inicializar_bd()

    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "TU_TOKEN_AQUI":
        print("❌ Error: TELEGRAM_BOT_TOKEN no configurado en variables de entorno.")
        return

    print("🚀 Iniciando Bot Telegram RadarAlertas en modo Nube 24/7...")

    # 1. Configurar aplicación Telegram
    global app_instance
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_instance = app

    app.add_handler(CommandHandler("start", comando_start))
    app.add_handler(CommandHandler("web", comando_web))
    app.add_handler(CommandHandler("app", comando_web))
    app.add_handler(CommandHandler("calculadora", comando_web))
    app.add_handler(CommandHandler("stats", comando_stats))
    app.add_handler(CommandHandler("activar", comando_activar_manual))
    app.add_handler(CommandHandler("invitar", comando_invitar))
    app.add_handler(CommandHandler("referidos", comando_invitar))
    app.add_handler(CommandHandler("auditar", comando_auditar))
    app.add_handler(CallbackQueryHandler(manejar_callback))
    app.add_handler(ChatMemberHandler(manejar_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.ALL, manejar_mensaje_general))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    print("✅ Bot de Telegram escuchando mensajes...")

    # Lanzar tareas en segundo plano (retargeting, renovaciones y emisión diaria gratuita)
    asyncio.create_task(tarea_retargeting_periodica(app))
    asyncio.create_task(tarea_renovaciones_periodica(app))
    asyncio.create_task(tarea_publicar_chollo_diario(app))

    # 2. Servidor web HTTP para la Landing Page, Webhook de Stripe y keep-alive en la nube
    puerto = int(os.getenv("PORT", 8080))
    server = web.Application()
    server.router.add_get("/", handle_landing_page)
    server.router.add_get("/index.html", handle_landing_page)
    server.router.add_get("/ping", handle_ping)
    server.router.add_get("/healthz", handle_ping)
    server.router.add_get("/api/visita", handle_track_visit)
    server.router.add_post("/api/visita", handle_track_visit)
    server.router.add_route("OPTIONS", "/api/visita", handle_track_visit)
    server.router.add_post("/webhook/stripe", handle_stripe_webhook)

    # Servir carpeta de assets estáticos (imágenes de oportunidades, fotos aéreas, logos)
    assets_dir = Path(__file__).resolve().parent.parent.parent / "assets"
    if assets_dir.exists():
        server.router.add_static("/assets", path=str(assets_dir), name="assets")

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
