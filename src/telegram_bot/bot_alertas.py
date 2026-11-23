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
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
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
    marcar_retargeting_enviado,
    registrar_referido,
    obtener_estadisticas_referidos,
    marcar_premio_referidos_entregado,
    guardar_provincia_favorita,
    obtener_provincia_favorita
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
STRIPE_LINK = os.getenv("STRIPE_PAYMENT_LINK", "https://buy.stripe.com/28E28s5Aq8ZBel18YRcQU03")
STRIPE_LINK_SUBASTAS = os.getenv("STRIPE_LINK_SUBASTAS", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_AYUDAS = os.getenv("STRIPE_LINK_AYUDAS", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_LICITACIONES = os.getenv("STRIPE_LINK_LICITACIONES", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_EMPLEO = os.getenv("STRIPE_LINK_EMPLEO", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_VEHICULOS = os.getenv("STRIPE_LINK_VEHICULOS", "https://buy.stripe.com/5kQdRa6Eu7VxdgXdf7cQU00")
STRIPE_LINK_PACK_TOTAL = os.getenv("STRIPE_LINK_PACK_TOTAL", "https://buy.stripe.com/28E28s5Aq8ZBel18YRcQU03")
STRIPE_LINK_PRO_ANUAL = os.getenv("STRIPE_LINK_PRO_ANUAL", "https://buy.stripe.com/aFa14o1kafnZccT0slcQU04")
WHATSAPP_CHANNEL_LINK = os.getenv("WHATSAPP_CHANNEL_LINK", "https://whatsapp.com/channel/0029Vb99ohpB4hdUuVdOHt2Q")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_USER_ID", "5674459275")
URL_WEB_APP = os.getenv("URL_WEB_APP", "https://radar-alertas-delta.vercel.app")

def con_ref(link: str, user_id: int) -> str:
    """Añade el ID de Telegram como client_reference_id al enlace de Stripe."""
    sep = "&" if "?" in link else "?"
    return f"{link}{sep}client_reference_id={user_id}"

async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /start con menú interactivo de botones y soporte para referidos."""
    user = update.effective_user
    registrar_o_actualizar_usuario(user.id, user.username, user.first_name)

    # 1. Comprobar si viene con enlace de referido: /start ref_123456
    if context.args:
        primer_arg = str(context.args[0]).strip()
        if primer_arg.startswith("ref_"):
            try:
                inviter_id = int(primer_arg.replace("ref_", ""))
                res_ref = registrar_referido(inviter_id, user.id)
                if res_ref.get("valido"):
                    total = res_ref.get("total_referidos", 1)
                    if res_ref.get("desbloquea_premio"):
                        activar_suscripcion_vip(inviter_id, plan="referidos_3_amigos", dias=30)
                        marcar_premio_referidos_entregado(inviter_id)
                        invite_link = CANAL_VIP_LINK
                        try:
                            l_obj = await context.bot.create_chat_invite_link(
                                chat_id=CANAL_VIP_ID,
                                member_limit=1,
                                name=f"Premio Referidos {inviter_id}"
                            )
                            invite_link = l_obj.invite_link
                        except Exception:
                            pass
                        premio_msg = (
                            "🎉🔥 *¡ENHORABUENA! HAS GANADO 1 MES VIP TOTAL GRATIS* 🔥🎉\n\n"
                            f"Tu amigo *{user.first_name}* se acaba de unir con tu enlace.\n"
                            "¡Has completado el objetivo de *3 amigos recomendados*!\n\n"
                            "⭐ *Tu acceso VIP TOTAL (Inmuebles, Vehículos, Ayudas, Licitaciones y Empleo) ha sido activado por 30 días a coste 0,00 €.*\n\n"
                            f"👉 Entra aquí a tu canal VIP exclusivo:\n{invite_link}\n\n"
                            "¡Muchísimas gracias por ayudar a crecer RadarAlertas!"
                        )
                        try:
                            await context.bot.send_message(chat_id=inviter_id, text=premio_msg, parse_mode="Markdown")
                            if str(ADMIN_ID) != str(inviter_id):
                                await context.bot.send_message(
                                    chat_id=ADMIN_ID,
                                    text=f"🏆 *¡Objetivo de Referidos Alcanzado!*\nEl usuario `{inviter_id}` ha traído a 3 personas y se le ha activado 1 mes VIP gratis automáticamente.",
                                    parse_mode="Markdown"
                                )
                        except Exception as e:
                            print(f"Error notificando premio al invitador: {e}")
                    else:
                        falta = max(0, 3 - total)
                        notif_msg = (
                            "🎉 *¡Un amigo se acaba de unir con tu enlace!*\n\n"
                            f"👤 *{user.first_name}* se ha registrado en RadarAlertas.\n"
                            f"📊 *Progreso:* Llevas *{total}/3* amigos.\n"
                            f"Te falta(n) solo *{falta}* para desbloquear tu *Mes VIP Gratis*."
                        )
                        try:
                            await context.bot.send_message(chat_id=inviter_id, text=notif_msg, parse_mode="Markdown")
                        except Exception as e:
                            print(f"Error enviando notificación al invitador: {e}")
            except Exception as e:
                print(f"Error procesando referido: {e}")

    # 2. Si viene con parámetro deep link de la landing page o redes
    if context.args:
        args_text = " ".join(str(arg).lower() for arg in context.args)
        
        # Deep link Guía de Coches
        if "coche" in args_text or "vehiculo" in args_text:
            if "guia" in args_text:
                registrar_descarga_guia(user.id)
                ruta_pdf_c = Path(__file__).resolve().parent.parent.parent / "assets" / "Guia_Coches_Embargados_RadarAlertas.pdf"
                if not ruta_pdf_c.exists():
                    from src.lead_magnet.generador_guia_coches_pdf import compilar_guia_coches_pdf
                    compilar_guia_coches_pdf(ruta_pdf_c)
                cap_c = (
                    f"🎁 *¡Hola {user.first_name}! Aquí tienes tu Guía Oficial de Coches y Vehículos Embargados en PDF.*\n\n"
                    "📖 *En este manual práctico aprenderás:*\n"
                    "• Cómo pujar en el BOE por coches, motos y furgonetas desde 500 €.\n"
                    "• Inspección en depósitos judiciales y auditoría de informe DGT.\n"
                    "• Cancelación de precintos y cargas por Decreto Judicial (Art. 674 LEC).\n\n"
                    "👇 Aquí tienes también el menú interactivo para consultar oportunidades:"
                )
                with open(ruta_pdf_c, "rb") as doc:
                    await update.message.reply_document(
                        document=doc,
                        filename="Guia_Coches_Embargados_RadarAlertas.pdf",
                        caption=cap_c,
                        parse_mode="Markdown"
                    )

        # Deep link Guía de Subastas Inmuebles
        elif any("guia" in str(arg).lower() for arg in context.args):
            registrar_descarga_guia(user.id)
            ruta_pdf = Path(__file__).resolve().parent.parent.parent / "assets" / "Guia_Subastas_Judiciales_RadarAlertas.pdf"
            if ruta_pdf.exists():
                cap = (
                    f"🎁 *¡Hola {user.first_name}! Aquí tienes tu Guía Oficial de Subastas y Embargos en PDF.*\n\n"
                    "📖 *En este manual práctico aprenderás:*\n"
                    "• Cómo funciona el portal del BOE y la fianza del 5%.\n"
                    "• El secreto del Art. 674 LEC: qué cargas se cancelan a 0 €.\n"
                    "• Cómo pujar por inmuebles desde el ordenador sin riesgos.\n\n"
                    "👇 Aquí tienes también el menú interactivo para consultar oportunidades:"
                )
                with open(ruta_pdf, "rb") as doc:
                    await update.message.reply_document(
                        document=doc,
                        filename="Guia_Subastas_Judiciales_RadarAlertas.pdf",
                        caption=cap,
                        parse_mode="Markdown"
                    )

    estado = obtener_estado_usuario(user.id)
    es_vip = estado and estado.get("suscripcion_activa") == 1

    mensaje = (
        f"👋 ¡Hola {user.first_name}! Bienvenido a *RadarAlertas*.\n\n"
        "Monitorizamos cada día fuentes oficiales del Estado con algoritmos inteligentes:\n"
        "🏠 *Subastas Inmuebles:* Pisos al -50% con Street View, Catastro y ROI.\n"
        "🚗 *Vehículos Embargados:* Coches y furgonetas verificados por matrícula desde 500 €.\n"
        "💰 *Ayudas y Subvenciones:* Fondos a fondo perdido (BDNS) con calendario.\n"
        "📑 *Licitaciones Públicas:* Contratos del Estado con pliegos oficiales.\n"
        "💼 *Empleo Público:* Plazas urgentes y convocatorias fijas (+2.150 € al mes).\n\n"
    )

    if es_vip:
        plan = estado.get("plan", "VIP")
        mensaje += f"⭐ *Tu estado:* MIEMBRO VIP ACTIVO ({plan}) - Válido hasta: {estado.get('fecha_fin_suscripcion')[:10]}\n\n"
        mensaje += "👇 *Accede a tus canales VIP exclusivos:*"
        
        teclado = [
            [InlineKeyboardButton("⚡ Explorador Web Interactivo (BOE/DGT) 🌐", web_app=WebAppInfo(url=URL_WEB_APP))],
            [InlineKeyboardButton("🏠 Subastas VIP", url=CANAL_VIP_LINK), InlineKeyboardButton("🚗 Vehículos VIP", url=CANAL_VEHICULOS_LINK)],
            [InlineKeyboardButton("💰 Ayudas VIP", url=CANAL_AYUDAS_LINK), InlineKeyboardButton("📑 Licitaciones VIP", url=CANAL_LICITACIONES_LINK)],
            [InlineKeyboardButton("💼 Empleo VIP", url=CANAL_EMPLEO_LINK)],
            [InlineKeyboardButton("🔍 Chollos por Provincia", callback_data="menu_provincias"), InlineKeyboardButton("🎁 Guías Gratis en PDF", callback_data="descargar_guia")],
            [InlineKeyboardButton("👥 Ganar Mes VIP (Invitar)", callback_data="menu_referidos"), InlineKeyboardButton("📊 Mi Suscripción", callback_data="mi_estado")]
        ]
    else:
        mensaje += (
            "👇 *Elige directamente el canal de alertas que te interesa:*\n"
            f"🔥 *Suscripciones individuales por {PRECIO_PROMO} € al mes* o el *Plan PRO Total por 14,99 € al mes* (o 99 €/año)."
        )
        teclado = [
            [
                InlineKeyboardButton("⚡ Explorador Web Interactivo (BOE/DGT) 🌐", web_app=WebAppInfo(url=URL_WEB_APP))
            ],
            [
                InlineKeyboardButton("💬 Canal Oficial de WhatsApp 📱", url=WHATSAPP_CHANNEL_LINK)
            ],
            [
                InlineKeyboardButton("🏠 Canal Inmuebles", callback_data="ver_canal_inmuebles"),
                InlineKeyboardButton("🚗 Canal Vehículos", callback_data="ver_canal_vehiculos")
            ],
            [
                InlineKeyboardButton("💰 Canal Ayudas", callback_data="ver_canal_ayudas"),
                InlineKeyboardButton("📑 Canal Licitaciones", callback_data="ver_canal_licitaciones")
            ],
            [
                InlineKeyboardButton("💼 Canal Empleo Público", callback_data="ver_canal_empleo")
            ],
            [
                InlineKeyboardButton("⭐ PLAN PRO: 5 CANALES VIP (14,99 €/m) ⭐", callback_data="pagar_vip")
            ],
            [
                InlineKeyboardButton("🔍 Chollos por Provincia", callback_data="menu_provincias"),
                InlineKeyboardButton("🎁 Guías Gratis en PDF", callback_data="descargar_guia")
            ],
            [
                InlineKeyboardButton("📢 Ver Alertas en Directo", url=CANAL_FREE_LINK),
                InlineKeyboardButton("📊 Mi Cuenta", callback_data="mi_estado")
            ]
        ]

    # Botón exclusivo para David (Administrador)
    if str(user.id) == str(ADMIN_ID):
        teclado.insert(0, [InlineKeyboardButton("📊 Panel de Estadísticas (Admin)", callback_data="ver_stats")])

    reply_markup = InlineKeyboardMarkup(teclado)
    await update.message.reply_text(mensaje, parse_mode="Markdown", reply_markup=reply_markup)

async def comando_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Abre el explorador web interactivo dentro de Telegram como Mini-App."""
    teclado = [
        [InlineKeyboardButton("⚡ Abrir Explorador Web Interactivo 🌐", web_app=WebAppInfo(url=URL_WEB_APP))]
    ]
    await update.message.reply_text(
        "🔍 *Explorador Web Oficial de RadarAlertas*\n\n"
        "Filtra en tiempo real por tu provincia subastas de pisos al -80%, coches de la DGT, ayudas públicas y licitaciones del Estado.\n\n"
        "👇 *Pulsa el botón abajo para abrir la Mini-App a pantalla completa:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(teclado)
    )

def generar_informe_auditoria(id_sub_input: str) -> tuple[str, list]:
    """Genera el texto formateado y los botones de auditoría para un expediente del BOE."""
    import re
    id_sub = re.sub(r"-+", "-", id_sub_input).strip().upper()

    det = obtener_detalle_subasta(id_sub)
    es_inmueble = True
    if not det or not det.get("direccion") or det.get("direccion") == "España":
        det_v = obtener_detalle_vehiculo(id_sub)
        if det_v and det_v.get("precio_salida", 0) > 0:
            det = det_v
            es_inmueble = False

    if det:
        score_badge = det.get("score_badge", "⭐ 8.5/10 (Oportunidad)")
        tasacion = det.get("valor_referencia_formato", "No consta")
        salida = det.get("precio_salida_formato", "0 €")
        ahorro = det.get("ahorro_porcentaje", 0)
        deposito = det.get("deposito", "5% LEC")

        if es_inmueble:
            sit_pos = det.get("situacion_posesoria", "⚪ No especificada")
            dir_txt = det.get("direccion", "España")
            url_maps = det.get("url_maps", "")
            url_cat = det.get("url_catastro", "")
            roi = det.get("roi_alquiler", 0)
            alquiler = det.get("alquiler_estimado_mes", 0)

            lineas_extra = f"📍 *Dirección:* `{dir_txt}`\n"
            if url_maps:
                lineas_extra += f"🗺️ [Ver Fachada en Google Street View]({url_maps})\n"
            if url_cat:
                lineas_extra += f"📑 [Consultar Ficha en Sede Catastro]({url_cat})\n"
            if roi > 0:
                lineas_extra += f"📈 *Potencial Inversor:* Alquiler est. ~{alquiler} €/mes | *ROI Bruto:* {roi}% anual\n"
            lineas_extra += f"🔍 *Estado Posesorio:* {sit_pos}\n"
        else:
            dep_loc = det.get("deposito_lugar", det.get("lugar_deposito", "Consultar juzgado")).strip()
            lineas_extra = (
                f"🚗 *Vehículo:* {det.get('titulo', 'Vehículo')}\n"
                f"📍 *Depósito:* `{dep_loc}`\n"
                f"🛡️ *Cargas DGT:* Cancelables mediante Decreto Judicial (Art. 674 LEC)\n"
            )

        res = (
            f"🔍 *INFORME DE AUDITORÍA EXPRÉS (BOE)* 🔍\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"{score_badge}\n\n"
            f"🆔 *Expediente:* `{id_sub}`\n"
            f"{lineas_extra}"
            f"💰 *Valor Oficial de Tasación:* {tasacion}\n"
            f"🟢 *Precio de Salida:* *{salida}* (-{ahorro}% dto.)\n"
            f"💵 *Fianza legal (5%):* *{deposito}* _(Reembolsable al 100% si no ganas)_\n"
            f"⏳ *Cierre de pujas:* {det.get('fecha_fin', 'Próximos días')}\n\n"
            f"🔗 [Abrir Expediente Oficial en subastas.boe.es]({det.get('url_oficial')})\n\n"
            f"⭐ _Para recibir alertas automáticas como esta en tu provincia, activa tu suscripción VIP._"
        )
        teclado = [
            [InlineKeyboardButton("⭐ Desbloquear Canales VIP (2,99 €/m)", callback_data="pagar_vip")],
            [InlineKeyboardButton("🔎 Auditar Otra Subasta", callback_data="pedir_auditoria")],
            [InlineKeyboardButton("🔙 Menú Principal", callback_data="volver_inicio")]
        ]
        return res, teclado
    else:
        res = (
            f"⚠️ No pudimos obtener el detalle del expediente `{id_sub}`.\n\n"
            "Es posible que la subasta haya concluido, que el código tenga algún error tipográfico, o el BOE no tenga habilitada la consulta pública para este lote.\n\n"
            "Comprueba que el formato sea similar a `SUB-JA-2024-224419` o prueba un ejemplo con los botones de abajo:"
        )
        teclado = [
            [
                InlineKeyboardButton("⚡ Probar Piso (Madrid)", callback_data="auditar_exp_SUB-JA-2024-224419"),
                InlineKeyboardButton("⚡ Probar Coche (Porsche)", callback_data="auditar_exp_SUB-JV-2026-268142")
            ],
            [InlineKeyboardButton("🔙 Menú Principal", callback_data="volver_inicio")]
        ]
        return res, teclado

async def manejar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestiona los clics en los botones interactivos."""
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user

    if data in ("escaparate_canales", "pagar_vip"):
        texto = (
            "📺 *ESCAPARATE OFICIAL DE CANALES RADARALERTAS* 📺\n\n"
            "Monitorizamos fuentes oficiales las 24 horas del día. Elige el canal específico para tu perfil o desbloquea todo con el **Plan PRO Total** con acceso completo e ilimitado:\n\n"
            "🏠 *1. Subastas de Inmuebles (2,99 €/mes)*\n"
            "• Pisos y chalets con >50% de descuento y sin cargas.\n"
            "• Enlaces directos a Google Street View, Catastro y ROI de alquiler.\n\n"
            "🚗 *2. Vehículos Embargados (2,99 €/mes)*\n"
            "• Coches, motos y furgonetas desde 500 € en depósitos judiciales.\n"
            "• Verificación de cargas DGT y comparador de cotización en Coches.net.\n\n"
            "💰 *3. Ayudas y Subvenciones (2,99 €/mes)*\n"
            "• Dinero a fondo perdido de la BDNS para autónomos y pymes.\n"
            "• Acceso a sede electrónica y recordatorio 1 clic en Google Calendar.\n\n"
            "📑 *4. Licitaciones Públicas (2,99 €/mes)*\n"
            "• Contratos menores de obras, servicios y tecnología.\n"
            "• Descarga directa de pliegos y condiciones oficiales en PDF.\n\n"
            "💼 *5. Empleo Público y Oposiciones (2,99 €/mes)*\n"
            "• Convocatorias fijas y bolsas urgentes del BOE (+2.150 €/mes).\n\n"
            "🔥 *PLAN PRO COMPLETO:* Acceso a los **5 Canales VIP + Buscador Web** por solo 14,99 €/mes (o 99 €/año)."
        )
        teclado = [
            [InlineKeyboardButton("⭐ Plan PRO Mensual (14,99 €/m)", url=con_ref(STRIPE_LINK_PACK_TOTAL, user.id))],
            [InlineKeyboardButton("🌟 Plan PRO Anual (99 €/año • Ahorra 80 €)", url=con_ref(STRIPE_LINK_PRO_ANUAL, user.id))],
            [InlineKeyboardButton("🏠 Inmuebles (2,99 €/m)", url=con_ref(STRIPE_LINK_SUBASTAS, user.id)), InlineKeyboardButton("🚗 Vehículos (2,99 €/m)", url=con_ref(STRIPE_LINK_VEHICULOS, user.id))],
            [InlineKeyboardButton("💰 Ayudas (2,99 €/m)", url=con_ref(STRIPE_LINK_AYUDAS, user.id)), InlineKeyboardButton("📑 Licitaciones (2,99 €/m)", url=con_ref(STRIPE_LINK_LICITACIONES, user.id))],
            [InlineKeyboardButton("💼 Empleo Público (2,99 €/m)", url=con_ref(STRIPE_LINK_EMPLEO, user.id))],
            [InlineKeyboardButton("📢 Ver Alertas en Directo (Gratis)", url=CANAL_FREE_LINK)],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "ver_canal_inmuebles":
        texto = (
            "🏠 *CANAL VIP: SUBASTAS INMOBILIARIAS* 🏠\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Rastreamos a diario el portal del BOE y la Seguridad Social para avisarte de pisos, chalets y locales con más del 50% de descuento respecto a mercado.\n\n"
            "✨ *QUÉ RECIBES EN CADA ALERTA:*\n"
            "• 📍 Dirección exacta con enlace directo a Google Street View.\n"
            "• 📑 Ficha catastral oficial con metros cuadrados y planos.\n"
            "• 📈 Rentabilidad de alquiler estimada (ROI anual).\n"
            "• 🔍 Auditoría posesoria (🟢 Libre de okupas vs 🔴 Ocupado).\n"
            "• 💵 Depósito legal del 5% (Art. 669.1 LEC, reembolsable al 100%).\n"
            "• ⏰ Enlace 1-clic a Google Calendar con alarma 2h antes del cierre.\n"
            "• 🔗 Enlace judicial directo al BOE para pujar sin intermediarios.\n\n"
            "👇 *Suscríbete ahora por 2,99 €/mes o accede a los 5 canales con el Plan PRO:*"
        )
        teclado = [
            [InlineKeyboardButton("⭐ Suscribirme a Inmuebles (2,99 €/mes)", url=con_ref(STRIPE_LINK_SUBASTAS, user.id))],
            [InlineKeyboardButton("⭐ Plan PRO Total: 5 Canales (14,99 €/mes)", url=con_ref(STRIPE_LINK_PACK_TOTAL, user.id))],
            [InlineKeyboardButton("📖 Descargar Guía Inmuebles Gratis (PDF)", callback_data="descargar_guia_pisos")],
            [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "ver_canal_vehiculos":
        texto = (
            "🚗 *CANAL VIP: VEHÍCULOS EMBARGADOS* 🚗\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Localizamos coches, turismos, SUV, furgonetas y motos en depósitos judiciales y campas municipales desde 500 € en toda España.\n\n"
            "✨ *QUÉ RECIBES EN CADA ALERTA:*\n"
            "• 🚙 Marca, modelo, combustible y matrícula verificada.\n"
            "• 📍 Ubicación en Google Maps de la campa para ir a inspeccionarlo.\n"
            "• 📊 Comparador directo de tasación en Coches.net.\n"
            "• 🛡️ Dictamen de cargas (Art. 674 LEC: se cancelan sin pagar deuda previa).\n"
            "• 💵 Depósito legal del 5% (100% reembolsable por el BOE si no ganas).\n"
            "• ⏰ Recordatorio en Google Calendar con alarma de fin de subasta.\n"
            "• 🔗 Enlace directo al expediente en el portal del BOE.\n\n"
            "👇 *Suscríbete ahora por 2,99 €/mes o accede a los 5 canales con el Plan PRO:*"
        )
        teclado = [
            [InlineKeyboardButton("⭐ Suscribirme a Vehículos (2,99 €/mes)", url=con_ref(STRIPE_LINK_VEHICULOS, user.id))],
            [InlineKeyboardButton("⭐ Plan PRO Total: 5 Canales (14,99 €/mes)", url=con_ref(STRIPE_LINK_PACK_TOTAL, user.id))],
            [InlineKeyboardButton("🚗 Descargar Guía Coches Gratis (PDF)", callback_data="descargar_guia_coches")],
            [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "ver_canal_ayudas":
        texto = (
            "💰 *CANAL VIP: AYUDAS Y SUBVENCIONES (BDNS)* 💰\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Monitorizamos la Base de Datos Nacional de Subvenciones para autónomos, pymes, empresas y particulares con dinero a fondo perdido.\n\n"
            "✨ *QUÉ RECIBES EN CADA ALERTA:*\n"
            "• 💶 Presupuesto oficial asignado y cuantía máxima por solicitante.\n"
            "• 👥 Requisitos y perfil de beneficiarios admitidos.\n"
            "• ⏳ Plazo de solicitud en días restantes (con cuenta atrás).\n"
            "• ⏰ Botón 1-clic para agendar la fecha límite en Google Calendar.\n"
            "• 🔗 Enlace directo a la Sede Electrónica oficial para tramitar.\n"
            "• 📑 Descarga directa de las bases reguladoras.\n\n"
            "👇 *Suscríbete ahora por 2,99 €/mes o accede a los 5 canales con el Plan PRO:*"
        )
        teclado = [
            [InlineKeyboardButton("⭐ Suscribirme a Ayudas (2,99 €/mes)", url=con_ref(STRIPE_LINK_AYUDAS, user.id))],
            [InlineKeyboardButton("⭐ Plan PRO Total: 5 Canales (14,99 €/mes)", url=con_ref(STRIPE_LINK_PACK_TOTAL, user.id))],
            [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "ver_canal_licitaciones":
        texto = (
            "📑 *CANAL VIP: LICITACIONES PÚBLICAS* 📑\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Filtrado inteligente de contratos menores de obras, servicios, suministros y tecnología abiertos a autónomos y pymes con cobro asegurado por el Estado.\n\n"
            "✨ *QUÉ RECIBES EN CADA ALERTA:*\n"
            "• 🏛️ Organismo convocante y objeto detallado del contrato.\n"
            "• 🆔 Número de expediente oficial en la Sección 5A del BOE.\n"
            "• 📥 Enlace directo de descarga del Pliego de Condiciones (PDF).\n"
            "• ⏰ Recordatorio en Google Calendar para preparar y presentar la oferta.\n\n"
            "👇 *Suscríbete ahora por 2,99 €/mes o accede a los 5 canales con el Plan PRO:*"
        )
        teclado = [
            [InlineKeyboardButton("⭐ Suscribirme a Licitaciones (2,99 €/mes)", url=con_ref(STRIPE_LINK_LICITACIONES, user.id))],
            [InlineKeyboardButton("⭐ Plan PRO Total: 5 Canales (14,99 €/mes)", url=con_ref(STRIPE_LINK_PACK_TOTAL, user.id))],
            [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "ver_canal_empleo":
        texto = (
            "💼 *CANAL VIP: EMPLEO PÚBLICO Y OPOSICIONES* 💼\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Detectamos cada mañana las convocatorias urgentes, bolsas de trabajo y plazas fijas publicadas en el BOE y boletines autonómicos (+2.150 € al mes).\n\n"
            "✨ *QUÉ RECIBES EN CADA ALERTA:*\n"
            "• 📋 Categoría profesional, titulación exigida y número de plazas.\n"
            "• 🏛️ Ministerio o administración pública convocante.\n"
            "• ⏳ Plazo de inscripción y presentación de instancias.\n"
            "• 📑 Enlace directo a la resolución oficial del BOE en PDF.\n\n"
            "👇 *Suscríbete ahora por 2,99 €/mes o accede a los 5 canales con el Plan PRO:*"
        )
        teclado = [
            [InlineKeyboardButton("⭐ Suscribirme a Empleo (2,99 €/mes)", url=con_ref(STRIPE_LINK_EMPLEO, user.id))],
            [InlineKeyboardButton("⭐ Plan PRO Total: 5 Canales (14,99 €/mes)", url=con_ref(STRIPE_LINK_PACK_TOTAL, user.id))],
            [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "mi_estado":
        estado = obtener_estado_usuario(user.id)
        if estado and estado.get("suscripcion_activa") == 1:
            texto = (
                f"✅ *Estado:* Suscripción VIP Activa\n"
                f"📅 *Válida hasta:* {estado.get('fecha_fin_suscripcion')[:10]}\n"
                f"💎 *Plan:* {estado.get('plan')}\n\n"
                f"Tienes acceso ilimitado a las alertas completas con Street View, Catastro y enlaces judiciales."
            )
            teclado = [
                [InlineKeyboardButton("📺 Acceder a mis Canales VIP", callback_data="volver_inicio")],
                [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="volver_inicio")]
            ]
        else:
            texto = (
                "❌ *Estado:* Cuenta Gratuita\n\n"
                "Aún no tienes activada la suscripción a los Canales VIP.\n"
                "Actívala desde solo 2,99 € al mes para recibir expedientes completos, referencias catastrales, Street View y enlaces directos para pujar."
            )
            teclado = [
                [InlineKeyboardButton("⭐ Desbloquear Canales VIP (desde 2,99 €)", callback_data="pagar_vip")],
                [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="volver_inicio")]
            ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "pedir_auditoria":
        texto = (
            "🔎 *AUDITOR JUDICIAL INSTANTÁNEO DEL BOE* 🔎\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "¿Has visto una subasta y quieres saber si es un chollo o una trampa con okupas o deudas?\n\n"
            "👉 *Solo tienes que escribirme o pegarme aquí el enlace o código del BOE.*\n"
            "Ejemplo: `SUB-JA-2024-224419`\n\n"
            "Nuestro algoritmo lo analizará en 3 segundos y te dirá:\n"
            "• Descuento real sobre tasación oficial\n"
            "• Estado de ocupación y riesgo de okupas\n"
            "• Fianza legal del 5% requerida (Art. 669.1 LEC)\n"
            "• Enlace a Google Street View y Catastro\n"
            "• Rentabilidad estimada de alquiler (ROI anual)\n\n"
            "👇 _Pega tu código aquí en el chat, prueba un ejemplo en 1 clic o vuelve al menú:_"
        )
        teclado = [
            [
                InlineKeyboardButton("⚡ Probar Piso (Madrid)", callback_data="auditar_exp_SUB-JA-2024-224419"),
                InlineKeyboardButton("⚡ Probar Coche (Porsche)", callback_data="auditar_exp_SUB-JV-2026-268142")
            ],
            [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data.startswith("auditar_exp_"):
        exp_id = data.replace("auditar_exp_", "")
        await query.answer("Auditoría en curso en el BOE...")
        res_txt, res_teclado = generar_informe_auditoria(exp_id)
        try:
            await query.edit_message_text(res_txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(res_teclado), disable_web_page_preview=True)
        except Exception:
            await query.edit_message_text(res_txt.replace("*", "").replace("`", "").replace("_", ""), reply_markup=InlineKeyboardMarkup(res_teclado), disable_web_page_preview=True)

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
        texto = (
            "🎁 *BIBLIOTECA DE GUÍAS PRÁCTICAS RADARALERTAS (PDF)* 🎁\n\n"
            "Descarga de forma 100% gratuita nuestros manuales prácticos oficiales para aprender a invertir con éxito:\n\n"
            "📖 *1. Guía Subastas Judiciales e Inmuebles del BOE*\n"
            "Aprende a pujar por pisos y chalets al -50%, cómo funciona el depósito del 5% del BOE y el secreto del Art. 674 LEC para cancelar cargas a 0 €.\n\n"
            "🚗 *2. Guía Coches y Vehículos Embargados*\n"
            "Cómo adquirir turismos y furgonetas desde 500 € en depósitos judiciales, verificación de informe DGT y cancelación de precintos legales.\n\n"
            "👇 *Elige la guía que deseas recibir al instante:*"
        )
        teclado = [
            [InlineKeyboardButton("📖 Descargar Guía Inmuebles (PDF)", callback_data="descargar_guia_pisos")],
            [InlineKeyboardButton("🚗 Descargar Guía Coches Embargados (PDF)", callback_data="descargar_guia_coches")],
            [InlineKeyboardButton("🔙 Volver al Menú", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "descargar_guia_pisos":
        await query.answer("Enviando Guía de Inmuebles...")
        registrar_descarga_guia(user.id)
        ruta_pdf = Path(__file__).resolve().parent.parent.parent / "assets" / "Guia_Subastas_Judiciales_RadarAlertas.pdf"
        if not ruta_pdf.exists():
            from src.lead_magnet.generador_guia_pdf import compilar_guia_pdf
            compilar_guia_pdf(ruta_pdf)

        cap = (
            "🎁 *¡Aquí tienes tu Guía Oficial de Subastas Judiciales e Inmuebles!*\n\n"
            "📖 *En este manual práctico aprenderás:*\n"
            "• Cómo funciona el portal del BOE y la devolución del 5% del depósito.\n"
            "• El secreto del Art. 674 LEC: qué cargas se cancelan y cuáles se pagan.\n"
            "• Auditoría anti-okupas y cálculo del precio máximo de puja.\n\n"
            "🚀 *¿Quieres que nuestro algoritmo te avise de chollos limpios cada día?*\n"
            "Únete a nuestros canales VIP exclusivos."
        )
        teclado = [
            [InlineKeyboardButton("⭐ Desbloquear Canales VIP", callback_data="pagar_vip")],
            [InlineKeyboardButton("🚗 Descargar También Guía de Coches", callback_data="descargar_guia_coches")],
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

    elif data == "descargar_guia_coches":
        await query.answer("Enviando Guía de Coches Embargados...")
        registrar_descarga_guia(user.id)
        ruta_pdf_c = Path(__file__).resolve().parent.parent.parent / "assets" / "Guia_Coches_Embargados_RadarAlertas.pdf"
        if not ruta_pdf_c.exists():
            from src.lead_magnet.generador_guia_coches_pdf import compilar_guia_coches_pdf
            compilar_guia_coches_pdf(ruta_pdf_c)

        cap_c = (
            "🎁 *¡Aquí tienes tu Guía Oficial de Coches y Vehículos Embargados!*\n\n"
            "📖 *En este manual práctico aprenderás:*\n"
            "• Cómo pujar en el BOE por coches, motos y furgonetas desde 500 €.\n"
            "• Auditoría de informe DGT y depósitos judiciales.\n"
            "• Cancelación de precintos y cargas por Decreto Judicial (Art. 674 LEC).\n\n"
            "🚀 *¿Quieres recibir avisos de vehículos filtrados cada día?*\n"
            "Únete a nuestro canal VIP de Motor."
        )
        teclado = [
            [InlineKeyboardButton("🚗 Activar Canal Vehículos (2,99 €/m)", url=con_ref(STRIPE_LINK_VEHICULOS, user.id))],
            [InlineKeyboardButton("⭐ Plan PRO Total: 5 Canales (14,99 €/m)", url=con_ref(STRIPE_LINK_PACK_TOTAL, user.id))],
            [InlineKeyboardButton("🔙 Volver al Menú", callback_data="volver_inicio")]
        ]
        with open(ruta_pdf_c, "rb") as doc:
            await context.bot.send_document(
                chat_id=user.id,
                document=doc,
                filename="Guia_Coches_Embargados_RadarAlertas.pdf",
                caption=cap_c,
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

        # Botón de alerta de provincia en 1 clic
        prov_actual = obtener_provincia_favorita(user.id)
        teclado = []
        if nom_prov != "España":
            if prov_actual and prov_actual.lower() == nom_prov.lower():
                teclado.append([InlineKeyboardButton(f"✅ Recibiendo alertas de {nom_prov}", callback_data=f"activada_prov_{nom_prov}")])
            else:
                teclado.append([InlineKeyboardButton(f"🔔 Avisarme de chollos en {nom_prov} (Gratis)", callback_data=f"activar_prov_{nom_prov}")])

        teclado.extend([
            [InlineKeyboardButton("⭐ Desbloquear Canales VIP", callback_data="pagar_vip")],
            [InlineKeyboardButton("📍 Buscar en otra Provincia", callback_data="menu_provincias")],
            [InlineKeyboardButton("🔙 Volver al Menú", callback_data="volver_inicio")]
        ])
        await query.edit_message_text(res_txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data.startswith("activar_prov_"):
        prov_nom = data.replace("activar_prov_", "").strip()
        guardar_provincia_favorita(user.id, prov_nom)
        await query.answer(f"🔔 ¡Listo! Te avisaremos de oportunidades en {prov_nom} a coste 0,00 €.", show_alert=True)
        teclado = [
            [InlineKeyboardButton(f"✅ Recibiendo alertas de {prov_nom}", callback_data=f"activada_prov_{prov_nom}")],
            [InlineKeyboardButton("⭐ Desbloquear Canales VIP", callback_data="pagar_vip")],
            [InlineKeyboardButton("📍 Buscar en otra Provincia", callback_data="menu_provincias")],
            [InlineKeyboardButton("🔙 Volver al Menú", callback_data="volver_inicio")]
        ]
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(teclado))

    elif data.startswith("activada_prov_"):
        prov_nom = data.replace("activada_prov_", "").strip()
        await query.answer(f"Ya tienes activadas las alertas para {prov_nom}.", show_alert=True)

    elif data == "menu_referidos":
        stats = obtener_estadisticas_referidos(user.id)
        bot_user = context.bot.username or "RadarAletasSubastas_bot"
        ref_link = f"https://t.me/{bot_user}?start=ref_{user.id}"
        total = stats.get("total_referidos", 0)
        premio = stats.get("premio_otorgado", False)
        
        texto_compartir = "¡Mira los chollos y coches embargados del BOE que encuentra este radar gratis!"
        url_compartir = f"https://t.me/share/url?url={ref_link}&text={texto_compartir}"
        
        txt = (
            "🎁 *PROGRAMA DE REFERIDOS: 1 MES VIP TOTAL GRATIS*\n\n"
            "Comparte RadarAlertas con amigos interesados en chollos, coches o subastas y "
            "consigue tu suscripción VIP Total (valorada en *14,99 €/mes*) a *coste 0,00 €*.\n\n"
            "📋 *¿Cómo funciona?*\n"
            "1. Pasa tu enlace exclusivo a tus amigos o compártelo en grupos.\n"
            "2. En cuanto *3 personas* se unan a través de tu link, el sistema te activará automáticamente *30 días de VIP Total*.\n\n"
            f"🔗 *Tu Enlace Personal de Invitación:*\n`{ref_link}`\n\n"
            f"📊 *Tu Marcador en Tiempo Real:*\n"
            f"• Amigos registrados: *{total} de 3*\n"
        )
        if premio or total >= 3:
            txt += "• Estado del premio: 🏆 *¡Objetivo cumplido! Tu mes VIP gratuito está activo.*\n"
        else:
            txt += f"• Te faltan: ⏳ *{3 - total} amigo(s)* para desbloquear tu mes gratis.\n"

        teclado = [
            [InlineKeyboardButton("📤 Compartir en Telegram (1 Clic)", url=url_compartir)],
            [InlineKeyboardButton("⭐ Desbloquear Ahora por 14,99 €/mes", callback_data="pagar_vip")],
            [InlineKeyboardButton("🔙 Volver al Menú", callback_data="volver_inicio")]
        ]
        await query.edit_message_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

    elif data == "volver_inicio":
        estado = obtener_estado_usuario(user.id)
        es_vip = estado and estado.get("suscripcion_activa") == 1

        if es_vip:
            plan = estado.get("plan", "VIP")
            texto_inicio = (
                f"👋 ¡Hola de nuevo, {user.first_name}!\n\n"
                f"⭐ *Tu estado:* MIEMBRO VIP ACTIVO ({plan}) - Válido hasta: {estado.get('fecha_fin_suscripcion')[:10]}\n\n"
                "👇 *Accede directamente a tus canales VIP exclusivos:*"
            )
            teclado = [
                [InlineKeyboardButton("⚡ Explorador Web Interactivo (BOE/DGT) 🌐", web_app=WebAppInfo(url=URL_WEB_APP))],
                [InlineKeyboardButton("💬 Canal Oficial de WhatsApp 📱", url=WHATSAPP_CHANNEL_LINK)],
                [InlineKeyboardButton("🏠 Subastas VIP", url=CANAL_VIP_LINK), InlineKeyboardButton("🚗 Vehículos VIP", url=CANAL_VEHICULOS_LINK)],
                [InlineKeyboardButton("💰 Ayudas VIP", url=CANAL_AYUDAS_LINK), InlineKeyboardButton("📑 Licitaciones VIP", url=CANAL_LICITACIONES_LINK)],
                [InlineKeyboardButton("💼 Empleo VIP", url=CANAL_EMPLEO_LINK)],
                [InlineKeyboardButton("🔍 Chollos por Provincia", callback_data="menu_provincias"), InlineKeyboardButton("🎁 Guías Gratis en PDF", callback_data="descargar_guia")],
                [InlineKeyboardButton("👥 Ganar Mes VIP (Invitar)", callback_data="menu_referidos"), InlineKeyboardButton("📊 Mi Suscripción", callback_data="mi_estado")]
            ]
        else:
            texto_inicio = (
                f"👋 ¡Hola {user.first_name}! Bienvenido a *RadarAlertas*.\n\n"
                "Monitorizamos cada día fuentes oficiales del Estado con algoritmos inteligentes:\n"
                "🏠 *Subastas Inmuebles:* Pisos al -50% con Street View, Catastro y ROI.\n"
                "🚗 *Vehículos Embargados:* Coches y furgonetas verificados por matrícula desde 500 €.\n"
                "💰 *Ayudas y Subvenciones:* Fondos a fondo perdido (BDNS) con calendario.\n"
                "📑 *Licitaciones Públicas:* Contratos del Estado con pliegos oficiales.\n"
                "💼 *Empleo Público:* Plazas urgentes y convocatorias fijas (+2.150 € al mes).\n\n"
                "👇 *Elige directamente el canal de alertas que te interesa:*"
            )
            teclado = [
                [
                    InlineKeyboardButton("⚡ Explorador Web Interactivo (BOE/DGT) 🌐", web_app=WebAppInfo(url=URL_WEB_APP))
                ],
                [
                    InlineKeyboardButton("💬 Canal Oficial de WhatsApp 📱", url=WHATSAPP_CHANNEL_LINK)
                ],
                [
                    InlineKeyboardButton("🏠 Canal Inmuebles", callback_data="ver_canal_inmuebles"),
                    InlineKeyboardButton("🚗 Canal Vehículos", callback_data="ver_canal_vehiculos")
                ],
                [
                    InlineKeyboardButton("💰 Canal Ayudas", callback_data="ver_canal_ayudas"),
                    InlineKeyboardButton("📑 Canal Licitaciones", callback_data="ver_canal_licitaciones")
                ],
                [
                    InlineKeyboardButton("💼 Canal Empleo Público", callback_data="ver_canal_empleo")
                ],
                [
                    InlineKeyboardButton("⭐ PLAN PRO: 5 CANALES VIP (14,99 €/m) ⭐", callback_data="pagar_vip")
                ],
                [
                    InlineKeyboardButton("🔍 Chollos por Provincia", callback_data="menu_provincias"),
                    InlineKeyboardButton("🎁 Guías Gratis en PDF", callback_data="descargar_guia")
                ],
                [
                    InlineKeyboardButton("📢 Ver Alertas en Directo", url=CANAL_FREE_LINK),
                    InlineKeyboardButton("📊 Mi Cuenta", callback_data="mi_estado")
                ]
            ]

        if str(user.id) == str(ADMIN_ID):
            teclado.insert(0, [InlineKeyboardButton("📊 Panel de Estadísticas (Admin)", callback_data="ver_stats")])

        reply_markup = InlineKeyboardMarkup(teclado)
        try:
            await query.edit_message_text(texto_inicio, parse_mode="Markdown", reply_markup=reply_markup)
        except Exception:
            await context.bot.send_message(chat_id=user.id, text=texto_inicio, parse_mode="Markdown", reply_markup=reply_markup)

async def comando_invitar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el panel de referidos y enlace personal de invitación."""
    user = update.effective_user
    stats = obtener_estadisticas_referidos(user.id)
    bot_user = context.bot.username or "RadarAletasSubastas_bot"
    ref_link = f"https://t.me/{bot_user}?start=ref_{user.id}"
    total = stats.get("total_referidos", 0)
    premio = stats.get("premio_otorgado", False)
    
    texto_compartir = "¡Mira los chollos y coches embargados del BOE que encuentra este radar gratis!"
    url_compartir = f"https://t.me/share/url?url={ref_link}&text={texto_compartir}"
    
    txt = (
        "🎁 *PROGRAMA DE REFERIDOS: 1 MES VIP TOTAL GRATIS*\n\n"
        "Comparte RadarAlertas con amigos interesados en chollos, coches o subastas y "
        "consigue tu suscripción VIP Total (valorada en *14,99 €/mes*) a *coste 0,00 €*.\n\n"
        "📋 *¿Cómo funciona?*\n"
        "1. Pasa tu enlace exclusivo a tus amigos o compártelo en grupos.\n"
        "2. En cuanto *3 personas* se unan a través de tu link, el sistema te activará automáticamente *30 días de VIP Total*.\n\n"
        f"🔗 *Tu Enlace Personal de Invitación:*\n`{ref_link}`\n\n"
        f"📊 *Tu Marcador en Tiempo Real:*\n"
        f"• Amigos registrados: *{total} de 3*\n"
    )
    if premio or total >= 3:
        txt += "• Estado del premio: 🏆 *¡Objetivo cumplido! Tu mes VIP gratuito está activo.*\n"
    else:
        txt += f"• Te faltan: ⏳ *{3 - total} amigo(s)* para desbloquear tu mes gratis.\n"

    teclado = [
        [InlineKeyboardButton("📤 Compartir en Telegram (1 Clic)", url=url_compartir)],
        [InlineKeyboardButton("⭐ Desbloquear Ahora por 14,99 €/mes", callback_data="pagar_vip")],
        [InlineKeyboardButton("🔙 Menú Principal", callback_data="volver_inicio")]
    ]
    await update.effective_message.reply_text(txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

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

    # 3. Mensaje de texto normal directo al bot (Auditor Exprés de Subastas)
    if msg.text and not msg.text.startswith("/"):
        import re
        txt = msg.text.strip()
        m = re.search(r"(SUB[-_]+[A-Z0-9-]+)", txt, re.IGNORECASE)
        if m:
            id_sub_raw = m.group(1)
            id_sub = re.sub(r"-+", "-", id_sub_raw).upper()
            try:
                msg_espera = await msg.reply_text(f"⏳ *Auditoría en curso:* Consultando expediente `{id_sub}` en el BOE...", parse_mode="Markdown")
            except Exception:
                msg_espera = await msg.reply_text(f"⏳ Auditoría en curso: Consultando expediente {id_sub} en el BOE...")
            
            res_txt, res_teclado = generar_informe_auditoria(id_sub)
            try:
                await msg_espera.edit_text(res_txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(res_teclado), disable_web_page_preview=True)
            except Exception:
                await msg_espera.edit_text(res_txt.replace("*", "").replace("`", "").replace("_", ""), reply_markup=InlineKeyboardMarkup(res_teclado), disable_web_page_preview=True)
        else:
            teclado_alt = [
                [
                    InlineKeyboardButton("🏠 Ver Canales y Alertas", callback_data="volver_inicio"),
                    InlineKeyboardButton("🔍 Chollos por Provincia", callback_data="menu_provincias")
                ],
                [
                    InlineKeyboardButton("🎁 Guías Gratis en PDF", callback_data="descargar_guia"),
                    InlineKeyboardButton("⭐ Plan PRO VIP (14,99 €)", callback_data="pagar_vip")
                ]
            ]
            await msg.reply_text(
                f"👋 ¡Hola {msg.from_user.first_name}! Bienvenido a *RadarAlertas*.\n\n"
                "Selecciona una opción del menú interactivo para empezar:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(teclado_alt)
            )

async def comando_auditar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando directo /auditar [codigo] para auditar cualquier subasta al instante."""
    msg = update.effective_message
    if not msg:
        return
    import re
    if context.args:
        codigo = " ".join(context.args).strip()
        m = re.search(r"(SUB[-_]+[A-Z0-9-]+)", codigo, re.IGNORECASE)
        cod = m.group(1) if m else codigo
        id_sub = re.sub(r"-+", "-", cod).upper()
        try:
            msg_espera = await msg.reply_text(f"⏳ *Auditoría en curso:* Consultando expediente `{id_sub}` en el BOE...", parse_mode="Markdown")
        except Exception:
            msg_espera = await msg.reply_text(f"⏳ Auditoría en curso: Consultando expediente {id_sub} en el BOE...")
        res_txt, res_teclado = generar_informe_auditoria(id_sub)
        try:
            await msg_espera.edit_text(res_txt, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(res_teclado), disable_web_page_preview=True)
        except Exception:
            await msg_espera.edit_text(res_txt.replace("*", "").replace("`", "").replace("_", ""), reply_markup=InlineKeyboardMarkup(res_teclado), disable_web_page_preview=True)
    else:
        texto = (
            "🔎 *AUDITOR JUDICIAL INSTANTÁNEO DEL BOE* 🔎\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "¿Has visto una subasta y quieres saber si es un chollo o una trampa con okupas o deudas?\n\n"
            "👉 *Solo tienes que escribirme o pegarme aquí el enlace o código del BOE.*\n"
            "Ejemplo: `SUB-JA-2024-224419`\n\n"
            "O pulsa directamente en uno de los ejemplos para ver el informe:"
        )
        teclado = [
            [
                InlineKeyboardButton("⚡ Probar Piso (Madrid)", callback_data="auditar_exp_SUB-JA-2024-224419"),
                InlineKeyboardButton("⚡ Probar Coche (Porsche)", callback_data="auditar_exp_SUB-JV-2026-268142")
            ],
            [InlineKeyboardButton("🔙 Menú Principal", callback_data="volver_inicio")]
        ]
        await msg.reply_text(texto, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(teclado))

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
        if "anual" in plan.lower():
            mrr += count * (99.0 / 12.0)
        elif "total" in plan.lower() or "pack" in plan.lower() or "pro" in plan.lower():
            mrr += count * 14.99
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
    app.add_handler(CommandHandler("auditar", comando_auditar))
    app.add_handler(CallbackQueryHandler(manejar_callback))
    app.add_handler(ChatMemberHandler(manejar_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.ALL, manejar_mensaje_general))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
