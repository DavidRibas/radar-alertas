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
    PreCheckoutQueryHandler,
    MessageHandler,
    ChatMemberHandler,
    filters
)

from src.telegram_bot.database import (
    inicializar_bd,
    registrar_o_actualizar_usuario,
    activar_suscripcion_vip,
    obtener_estado_usuario,
    obtener_metricas_globales,
    registrar_descarga_guia,
    obtener_usuarios_para_retargeting,
    marcar_retargeting_enviado
)
from src.extractores.boe_inmuebles import buscar_subastas_inmuebles, obtener_detalle_subasta
from src.extractores.boe_vehiculos import buscar_subastas_vehiculos, obtener_detalle_vehiculo

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TU_TOKEN_AQUI")
CANAL_VIP_ID = os.getenv("TELEGRAM_CANAL_VIP_ID", "@canal_vip_demo")
CANAL_VIP_LINK = os.getenv("TELEGRAM_CANAL_VIP_LINK", "https://t.me/+miVPfMylHboyMzM0")
CANAL_AYUDAS_ID = os.getenv("TELEGRAM_CANAL_AYUDAS_ID", "-1004437054989")
CANAL_AYUDAS_LINK = os.getenv("TELEGRAM_CANAL_AYUDAS_LINK", "https://t.me/+sSZjzzP5XediMDc0")
CANAL_LICITACIONES_ID = os.getenv("TELEGRAM_CANAL_LICITACIONES_ID", "-1004308901950")
CANAL_LICITACIONES_LINK = os.getenv("TELEGRAM_CANAL_LICITACIONES_LINK", "https://t.me/+SoEJ3dNfqdRlY2I0")
CANAL_EMPLEO_ID = os.getenv("TELEGRAM_CANAL_EMPLEO_ID", "-1004292956298")
CANAL_EMPLEO_LINK = os.getenv("TELEGRAM_CANAL_EMPLEO_LINK", "https://t.me/+S46Itb8Avi9iNmFk")
CANAL_VEHICULOS_ID = os.getenv("TELEGRAM_CANAL_VEHICULOS_ID", "-1004491031420")
CANAL_VEHICULOS_LINK = os.getenv("TELEGRAM_CANAL_VEHICULOS_LINK", "https://t.me/+rre7hII7bqhkNTdk")
CANAL_FREE_ID = os.getenv("TELEGRAM_CANAL_FREE_ID", "-1004345947331")
CANAL_FREE_LINK = os.getenv("TELEGRAM_CANAL_FREE_LINK", "https://t.me/+JoX17328N-VkMWVk")

PRECIO_PROMO = os.getenv("PRECIO_PROMOCION", "2.99")
STRIPE_LINK = os.getenv("STRIPE_PAYMENT_LINK", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_SUBASTAS = os.getenv("STRIPE_LINK_SUBASTAS", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_AYUDAS = os.getenv("STRIPE_LINK_AYUDAS", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_LICITACIONES = os.getenv("STRIPE_LINK_LICITACIONES", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_EMPLEO = os.getenv("STRIPE_LINK_EMPLEO", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_VEHICULOS = os.getenv("STRIPE_LINK_VEHICULOS", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_PACK_TOTAL = os.getenv("STRIPE_LINK_PACK_TOTAL", "https://buy.stripe.com/14A4gA0g6a3Fgt9a2VcQU01")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_USER_ID", "5674459275")

async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /start con menú interactivo de botones."""
    user = update.effective_user
    registrar_o_actualizar_usuario(user.id, user.username, user.first_name)

    estado = obtener_estado_usuario(user.id)
    es_vip = estado and estado.get("suscripcion_activa") == 1

    mensaje = (
        f"👋 ¡Hola {user.first_name}! Bienvenido a *RadarAlertas*.\n\n"
        "Monitorizamos cada día fuentes oficiales del Estado con algoritmos inteligentes:\n"
        "🏠 *Subastas Judiciales:* Inmuebles con más del 50% de ahorro y sin cargas.\n"
        "💰 *Ayudas y Subvenciones:* Dinero a fondo perdido (BDNS) con trámites directos.\n"
        "📑 *Licitaciones Públicas:* Contratos menores de obras, servicios y suministros.\n"
        "💼 *Empleo Público:* Plazas urgentes y bolsas de trabajo en el BOE.\n\n"
    )

    if es_vip:
        plan = estado.get("plan", "VIP")
        mensaje += f"⭐ *Tu estado:* MIEMBRO VIP ACTIVO ({plan}) - Válido hasta: {estado.get('fecha_fin_suscripcion')[:10]}\n\n"
        mensaje += "👇 *Accede a tus canales VIP exclusivos:*"
        
        teclado = [
            [InlineKeyboardButton("🏠 Subastas VIP", url=CANAL_VIP_LINK), InlineKeyboardButton("🚗 Vehículos VIP", url=CANAL_VEHICULOS_LINK)],
            [InlineKeyboardButton("💰 Ayudas VIP", url=CANAL_AYUDAS_LINK), InlineKeyboardButton("📑 Licitaciones VIP", url=CANAL_LICITACIONES_LINK)],
            [InlineKeyboardButton("💼 Empleo VIP", url=CANAL_EMPLEO_LINK)],
            [InlineKeyboardButton("🔍 Buscar Chollos por Provincia", callback_data="menu_provincias")],
            [InlineKeyboardButton("🎁 Descargar Guía Gratuita en PDF", callback_data="descargar_guia")],
            [InlineKeyboardButton("📊 Mi Suscripción", callback_data="mi_estado")]
        ]
    else:
        mensaje += (
            "🔒 *Acceso exclusivo:* Suscríbete para recibir alertas en tiempo real "
            "con expedientes completos, referencias catastrales y enlaces oficiales.\n\n"
            f"🔥 *Suscripciones desde solo {PRECIO_PROMO} € / mes* o el *Pack Total por 4,99 € / mes*."
        )
        teclado = [
            [InlineKeyboardButton("⭐ Desbloquear Canales VIP", callback_data="pagar_vip")],
            [InlineKeyboardButton("🎁 Descargar Guía Gratuita en PDF", callback_data="descargar_guia")],
            [InlineKeyboardButton("🔍 Buscar Chollos por Provincia", callback_data="menu_provincias")],
            [InlineKeyboardButton("📢 Canal Gratuito de Muestras", url=CANAL_FREE_LINK)],
            [InlineKeyboardButton("ℹ️ ¿Cómo funciona el servicio?", callback_data="info_servicio")],
            [InlineKeyboardButton("📊 Mi Cuenta", callback_data="mi_estado")]
        ]

    # Botón exclusivo para David (Administrador)
    if str(user.id) == str(ADMIN_ID):
        teclado.insert(0, [InlineKeyboardButton("📊 Panel de Estadísticas (Admin)", callback_data="ver_stats")])

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
            "🚀 *Planes de Acceso Oficial a RadarAlertas VIP*\n\n"
            "Puedes suscribirte a cualquier canal individual por **2,99 € / mes**, o desbloquear los 5 canales con el **Pack Total** ahorrando un 66%:\n\n"
            "🏠 *Canal Subastas Inmobiliarias:* Pisos al -50%, chalets y locales.\n"
            "🚗 *Canal Vehículos Embargados:* Coches, motos y furgonetas desde 500 €.\n"
            "💰 *Canal Ayudas y Subvenciones:* Dinero a fondo perdido y trámites de sede.\n"
            "📑 *Canal Licitaciones Públicas:* Contratos menores de obras, servicios e IT.\n"
            "💼 *Canal Empleo y Oposiciones:* Plazas fijas, bolsas urgentes y convocatorias.\n\n"
            "💡 *Recomendación:* El Pack Total te da acceso ilimitado a las 5 verticales por solo 4,99 €/mes."
        )
        teclado = [
            [InlineKeyboardButton("🏠 Solo Subastas Inmuebles (2,99 €/mes)", url=STRIPE_LINK_SUBASTAS)],
            [InlineKeyboardButton("🚗 Solo Vehículos Embargados (2,99 €/mes)", url=STRIPE_LINK_VEHICULOS)],
            [InlineKeyboardButton("💰 Solo Ayudas y Subvenciones (2,99 €/mes)", url=STRIPE_LINK_AYUDAS)],
            [InlineKeyboardButton("📑 Solo Licitaciones Públicas (2,99 €/mes)", url=STRIPE_LINK_LICITACIONES)],
            [InlineKeyboardButton("💼 Solo Empleo y Oposiciones (2,99 €/mes)", url=STRIPE_LINK_EMPLEO)],
            [InlineKeyboardButton("🔥 PACK TOTAL: LOS 5 CANALES (4,99 €/mes) 🔥", url=STRIPE_LINK_PACK_TOTAL)],
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

    elif data == "ver_stats":
        if str(user.id) != str(ADMIN_ID):
            await query.answer("Acceso denegado", show_alert=True)
            return
        texto = await generar_texto_stats(context)
        teclado = [[InlineKeyboardButton("🔙 Volver", callback_data="volver_inicio")]]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "descargar_guia":
        await query.answer("Enviando guía oficial en PDF...")
        registrar_descarga_guia(user.id)
        ruta_pdf = Path(__file__).resolve().parent.parent.parent / "assets" / "Guia_Subastas_Judiciales_RadarAlertas.pdf"
        if not ruta_pdf.exists():
            from src.lead_magnet.generador_guia_pdf import compilar_guia_pdf
            compilar_guia_pdf(ruta_pdf)

        cap = (
            "🎁 *¡Aquí tienes tu Guía Oficial de Subastas y Embargos!*\n\n"
            "📖 *En este manual práctico aprenderás:*\n"
            "• Cómo funciona el portal del BOE y la devolución del 5% del depósito.\n"
            "• El secreto del Art. 674 LEC: qué cargas se cancelan y cuáles se pagan.\n"
            "• Cómo pujar por coches y vehículos desde 500 € con inspección previa.\n\n"
            "🚀 *¿Quieres que nuestro algoritmo te avise de chollos limpios cada día?*\n"
            "Únete a nuestros canales VIP exclusivos."
        )
        teclado = [
            [InlineKeyboardButton("⭐ Desbloquear Canales VIP (desde 2,99 €/mes)", callback_data="pagar_vip")],
            [InlineKeyboardButton("📢 Canal Gratuito de Muestras", url=CANAL_FREE_LINK)],
            [InlineKeyboardButton("🔙 Volver al Menú", callback_data="volver_inicio")]
        ]
        with open(ruta_pdf, "rb") as doc:
            await context.bot.send_document(
                chat_id=user.id,
                document=doc,
                filename="Guia_Subastas_Judiciales_RadarAlertas.pdf",
                caption=cap,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(teclado)
            )

    elif data == "menu_provincias":
        texto = (
            "📍 *Buscador Oficial de Chollos por Provincia*\n\n"
            "Selecciona tu zona para consultar oportunidades activas hoy en el BOE "
            "(subastas de inmuebles y vehículos en celebración):"
        )
        teclado = [
            [InlineKeyboardButton("📍 Madrid", callback_data="buscar_prov_28"), InlineKeyboardButton("📍 Barcelona", callback_data="buscar_prov_08")],
            [InlineKeyboardButton("📍 Valencia", callback_data="buscar_prov_46"), InlineKeyboardButton("📍 Sevilla", callback_data="buscar_prov_41")],
            [InlineKeyboardButton("📍 Málaga", callback_data="buscar_prov_29"), InlineKeyboardButton("📍 Alicante", callback_data="buscar_prov_03")],
            [InlineKeyboardButton("🇪🇸 Toda España", callback_data="buscar_prov_all")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data.startswith("buscar_prov_"):
        prov_cod = data.replace("buscar_prov_", "")
        prov_map = {
            "28": "Madrid", "08": "Barcelona", "46": "Valencia",
            "41": "Sevilla", "29": "Málaga", "03": "Alicante", "all": "Toda España"
        }
        nom_prov = prov_map.get(prov_cod, "España")
        cod_filtro = "" if prov_cod == "all" else prov_cod

        await query.answer(f"Consultando oportunidades en {nom_prov}...")

        # Consultar subastas activas
        ids_inm = buscar_subastas_inmuebles(provincia_cod=cod_filtro, limite=2)
        ids_veh = buscar_subastas_vehiculos(provincia_cod=cod_filtro, limite=2)

        lineas = []
        for i_id in ids_inm[:2]:
            det = obtener_detalle_subasta(i_id)
            if det:
                lineas.append(
                    f"🏠 *{det['titulo']}*\n"
                    f"• Tasación: {det['valor_referencia_formato']} -> Salida: *{det['precio_salida_formato']}* (-{det['ahorro_porcentaje']}%)\n"
                    f"• Expediente ID: `{det['id_subasta']}`"
                )

        for v_id in ids_veh[:2]:
            v_det = obtener_detalle_vehiculo(v_id)
            if v_det:
                lineas.append(
                    f"🚗 *{v_det['titulo']} ({v_det['provincia']})*\n"
                    f"• Tasación: {v_det['valor_referencia_formato']} -> Salida: *{v_det['precio_salida_formato']}* (-{v_det['ahorro_porcentaje']}%)\n"
                    f"• Expediente ID: `{v_det['id_subasta']}`"
                )

        if not lineas:
            res_txt = f"⚠️ Actualmente no constan expedientes abiertos con descuento en {nom_prov}. Revisa el canal gratuito o consulta Toda España."
        else:
            res_txt = (
                f"🔎 *OPORTUNIDADES DESTACADAS EN {nom_prov.upper()}:*\n\n"
                + "\n\n".join(lineas)
                + "\n\n🔒 *Los enlaces directos de puja, referencias catastrales y matrículas se publican en tiempo real en los Canales VIP.*"
            )

        teclado = [
            [InlineKeyboardButton("⭐ Desbloquear Canales VIP", callback_data="pagar_vip")],
            [InlineKeyboardButton("📍 Buscar en otra Provincia", callback_data="menu_provincias")],
            [InlineKeyboardButton("🔙 Volver al Menú", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(res_txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "volver_inicio":
        teclado = [
            [InlineKeyboardButton("⭐ Desbloquear Canales VIP", callback_data="pagar_vip")],
            [InlineKeyboardButton("🎁 Descargar Guía Gratuita en PDF", callback_data="descargar_guia")],
            [InlineKeyboardButton("🔍 Buscar Chollos por Provincia", callback_data="menu_provincias")],
            [InlineKeyboardButton("📢 Canal Gratuito de Muestras", url=CANAL_FREE_LINK)],
            [InlineKeyboardButton("ℹ️ ¿Cómo funciona el servicio?", callback_data="info_servicio")],
            [InlineKeyboardButton("📊 Mi Cuenta", callback_data="mi_estado")]
        ]
        if str(user.id) == str(ADMIN_ID):
            teclado.insert(0, [InlineKeyboardButton("📊 Panel de Estadísticas (Admin)", callback_data="ver_stats")])
        await query.edit_message_text("Selecciona una opción del menú:", reply_markup=InlineKeyboardMarkup(teclado))

async def manejar_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detecta cuando el bot es añadido o modificado como administrador en un canal."""
    chat = update.effective_chat
    if chat and chat.type == "channel":
        print(f"🎯 CANAL DETECTADO POR ADMINISTRADOR: '{chat.title}' ID: {chat.id}")
        if ADMIN_ID:
            try:
                await context.bot.send_message(
                    chat_id=int(ADMIN_ID),
                    text=f"🎯 *¡Canal Detectado al Añadir Bot como Admin!*\n\n"
                         f"📌 *Nombre:* {chat.title}\n"
                         f"🆔 *ID:* `{chat.id}`\n\n"
                         f"Copia este ID para configurarlo en el sistema.",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Error avisando a admin: {e}")

async def manejar_mensaje_general(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detecta canales cuando el bot está dentro o cuando se le reenvía un mensaje."""
    # 1. Si alguien escribe en un canal donde el bot es admin
    if update.channel_post:
        chat = update.channel_post.chat
        print(f"🎯 CANAL DETECTADO POR POST: '{chat.title}' ID: {chat.id}")
        if ADMIN_ID:
            try:
                await context.bot.send_message(
                    chat_id=int(ADMIN_ID),
                    text=f"🎯 *¡Canal Detectado por Mensaje!*\n\n"
                         f"📌 *Nombre:* {chat.title}\n"
                         f"🆔 *ID:* `{chat.id}`\n\n"
                         f"Copia este ID para configurarlo.",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Error avisando a admin: {e}")
        return

    msg = update.effective_message
    if not msg:
        return

    # 2. Reenvíos desde un canal (soporta Telegram v20 y v21+)
    origen_chat = None
    if hasattr(msg, "forward_origin") and msg.forward_origin:
        origen_chat = getattr(msg.forward_origin, "chat", None)
    elif msg.forward_from_chat:
        origen_chat = msg.forward_from_chat

    if origen_chat:
        await msg.reply_text(
            f"🎯 *Canal detectado con éxito:*\n\n"
            f"📌 *Nombre:* {origen_chat.title}\n"
            f"🆔 *ID:* `{origen_chat.id}`",
            parse_mode="Markdown"
        )
        return

    # 3. Mensaje de texto normal directo al bot
    if msg.text and not msg.text.startswith("/"):
        await msg.reply_text("¡Hola! Usa /start para ver el menú principal de RadarAlertas.")

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

async def generar_texto_stats(context: ContextTypes.DEFAULT_TYPE) -> str:
    """Genera el texto de estadísticas del negocio con los miembros reales de cada canal."""
    m = obtener_metricas_globales()

    mrr = 0.0
    for plan, count in m["desglose_planes"].items():
        if "total" in plan.lower() or "pack" in plan.lower():
            mrr += count * 4.99
        else:
            mrr += count * 2.99

    canales = [
        ("🏠 Subastas VIP", CANAL_VIP_ID),
        ("🚗 Vehículos VIP", CANAL_VEHICULOS_ID),
        ("💰 Ayudas VIP", CANAL_AYUDAS_ID),
        ("📑 Licitaciones VIP", CANAL_LICITACIONES_ID),
        ("💼 Empleo VIP", CANAL_EMPLEO_ID),
        ("📢 Canal Gratuito", CANAL_FREE_ID)
    ]
    conteo_lineas = []
    for nombre, cid in canales:
        try:
            cnt = await context.bot.get_chat_member_count(cid)
            conteo_lineas.append(f"• {nombre}: *{cnt} miembros*")
        except Exception:
            conteo_lineas.append(f"• {nombre}: *Activo*")

    conteo_str = "\n".join(conteo_lineas)

    texto = (
        "📊 *PANEL DE CONTROL - RADARALERTAS*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "👥 *Métricas de Usuarios:*\n"
        f"• Total registrados en bot: *{m['total_usuarios']}*\n"
        f"• Nuevos registros hoy: *+{m['usuarios_hoy']}*\n"
        f"• Suscriptores VIP activos: *{m['vip_activos']}*\n\n"
        "💶 *Facturación Recurrente (MRR):*\n"
        f"• MRR Estimado: *{mrr:.2f} € / mes*\n\n"
        "👥 *Miembros Reales en Canales:*\n"
        f"{conteo_str}\n\n"
        "📡 *Actividad de Emisión:*\n"
        f"• Oportunidades enviadas hoy: *{m['alertas_hoy']}*\n"
        f"• Histórico total alertas: *{m['total_alertas']}*\n\n"
        "🟢 *Estado Servidor:* Online 24/7 (Render Cloud)\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    return texto

async def comando_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el panel de control y métricas del negocio solo al administrador."""
    user = update.effective_user
    if str(user.id) != str(ADMIN_ID):
        await update.message.reply_text("⛔ Este comando es exclusivo para el administrador del sistema.")
        return

    texto = await generar_texto_stats(context)
    await update.message.reply_text(texto, parse_mode="Markdown")

def main():
    inicializar_bd()
    if TELEGRAM_TOKEN == "TU_TOKEN_AQUI":
        print("⚠️ AVISO: Configura TELEGRAM_BOT_TOKEN en tu archivo .env para conectar con Telegram.")
        print("👉 Para crear tu bot gratis: Abre Telegram, busca @BotFather, escribe /newbot y copia el token.")
        return

    print("🤖 Iniciando Bot de Telegram RadarAlertas...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", comando_start))
    app.add_handler(CommandHandler("stats", comando_stats))
    app.add_handler(CommandHandler("activar", comando_activar_manual))
    app.add_handler(CallbackQueryHandler(manejar_callback))
    app.add_handler(ChatMemberHandler(manejar_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.ALL, manejar_mensaje_general))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
