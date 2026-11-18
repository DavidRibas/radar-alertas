"""
Orquestador Multi-Vertical Oficial de RadarAlertas:
Controla las 4 verticales del negocio con selección horaria inteligente:
  • 09:00 AM -> 🏠 Subastas Judiciales e Inmuebles
  • 14:00 PM -> 💰 Ayudas y Subvenciones a Fondo Perdido (BDNS)
  • 18:30 PM -> 📑 Licitaciones Públicas y Empleo del Estado (BOE)
Coste: 0,00 €.
"""
import os
import sys
import asyncio
import datetime
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_ROOT = Path(__file__).resolve().parent.parent
if str(BASE_ROOT) not in sys.path:
    sys.path.insert(0, str(BASE_ROOT))

load_dotenv()

# Importar extractores y generadores
from src.extractores.boe_inmuebles import buscar_subastas_inmuebles, filtrar_mejores_chollos
from src.extractores.ayudas_subvenciones import obtener_convocatorias_recientes, filtrar_mejores_ayudas
from src.extractores.licitaciones_contratos import obtener_licitaciones_recientes
from src.extractores.empleo_oposiciones import obtener_empleo_publico_reciente
from src.extractores.boe_vehiculos import buscar_subastas_vehiculos, filtrar_mejores_vehiculos

from src.telegram_bot.database import inicializar_bd, registrar_alerta_enviada, ya_fue_enviada
from src.telegram_bot.formateador import formatear_post_vip, formatear_post_gratuito
from src.telegram_bot.formateador_ayudas import formatear_post_ayuda_vip, formatear_post_ayuda_gratuito
from src.telegram_bot.formateador_licitaciones import formatear_post_licitacion_vip, formatear_post_licitacion_gratuito
from src.telegram_bot.formateador_empleo import formatear_post_empleo_vip, formatear_post_empleo_gratuito
from src.telegram_bot.formateador_vehiculos import formatear_post_vehiculo_vip, formatear_post_vehiculo_gratuito

from src.video_generator.generador_visual_earth import (
    preparar_escena_1_satelite,
    preparar_escena_2_fachada,
    preparar_escena_3_interior,
    preparar_escena_4_telegram,
    generar_locucion_y_subtitulos,
    convertir_srt_a_ass,
    ensamblar_video_cinematico,
    obtener_duracion_audio,
    OUTPUT_DIR
)
from src.video_generator.generador_visual_ayudas import generar_video_ayuda_visual
from src.video_generator.generador_visual_licitaciones import generar_video_licitacion_visual
from src.video_generator.generador_visual_empleo import generar_video_empleo_visual
from src.video_generator.generador_visual_vehiculos import generar_video_vehiculo_visual
from src.utils.limpiador_disco import purgar_archivos_antiguos, limpiar_temporales_render

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_USER_ID")
CANAL_VIP = os.getenv("TELEGRAM_CANAL_VIP_ID")
CANAL_FREE = os.getenv("TELEGRAM_CANAL_FREE_ID")

def enviar_alerta_telegram(canal_id: str, texto_markdown: str):
    """Envía la alerta al canal VIP correspondiente."""
    if not TOKEN or not canal_id or canal_id == "@canal_vip_demo":
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": canal_id, "text": texto_markdown, "parse_mode": "Markdown"}, timeout=10)
        print(f"✈️ Alerta enviada a Telegram ({canal_id})")
    except Exception as e:
        print(f"⚠️ Error al enviar alerta Telegram: {e}")

def enviar_video_al_admin(ruta_video: Path, caption: str):
    """Envía el vídeo generado y el texto de TikTok/Reels directamente al móvil de David."""
    if not TOKEN or not ADMIN_ID or not ruta_video.exists():
        return
    try:
        print(f"📱 Enviando vídeo al móvil de David ({ADMIN_ID})...")
        url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
        with open(ruta_video, "rb") as vf:
            requests.post(
                url,
                data={"chat_id": ADMIN_ID, "caption": caption, "parse_mode": "Markdown"},
                files={"video": vf},
                timeout=45
            )
        print("✅ ¡Vídeo recibido en tu Telegram con éxito!")
    except Exception as e:
        print(f"⚠️ Error al enviar vídeo al móvil: {e}")

async def ciclo_subastas(provincia: str = "28"):
    print("\n" + "="*50 + "\n🏠 [VERTICAL 1] SUBASTAS JUDICIALES BOE\n" + "="*50)
    ids = buscar_subastas_inmuebles(provincia_cod=provincia, limite=20)
    if not ids:
        print("⚠️ No hay subastas nuevas.")
        return
    mejores = filtrar_mejores_chollos(ids, max_resultados=1)
    if not mejores:
        return
    chollo = mejores[0]
    id_sub = chollo["id_subasta"]

    # Generar vídeo si no fue procesado
    e1, e2, e3, e4 = OUTPUT_DIR/f"{id_sub}_e1.png", OUTPUT_DIR/f"{id_sub}_e2.png", OUTPUT_DIR/f"{id_sub}_e3.png", OUTPUT_DIR/f"{id_sub}_e4.png"
    preparar_escena_1_satelite(e1)
    preparar_escena_2_fachada(e2)
    preparar_escena_3_interior(e3)
    preparar_escena_4_telegram(e4)

    ruta_audio = OUTPUT_DIR / f"{id_sub}_audio.mp3"
    ruta_srt = OUTPUT_DIR / f"{id_sub}_sub.srt"
    ruta_ass = OUTPUT_DIR / f"{id_sub}_sub.ass"
    ruta_video = OUTPUT_DIR / f"{id_sub}_TIKTOK_FINAL.mp4"

    guion = (
        f"Mira lo que acaba de publicar el BOE para {chollo['localidad']}. "
        f"Sale a subasta este inmueble tasado en {chollo['valor_referencia_formato']} "
        f"por tan solo {chollo['precio_salida_formato']}. "
        f"Es un ahorro del {chollo['ahorro_porcentaje']} por ciento respecto a su valor real. "
        "El expediente no presenta cargas hipotecarias preferentes. "
        "Tienes el enlace judicial directo y el expediente completo en nuestro canal de Telegram. "
        "Entra en el enlace de nuestro perfil."
    )
    await generar_locucion_y_subtitulos(guion, ruta_audio, ruta_srt)
    convertir_srt_a_ass(ruta_srt, ruta_ass)

    dur_a = obtener_duracion_audio(ruta_audio)
    duraciones = [3.5, 5.0, 6.5, max(7.0, (dur_a - 15.0) + 2.0)]
    ensamblar_video_cinematico([e1, e2, e3, e4], duraciones, ruta_audio, ruta_ass, ruta_video)

    # Publicar y enviar al móvil
    post = formatear_post_vip(chollo)
    enviar_alerta_telegram(CANAL_VIP, post)
    if CANAL_FREE:
        post_free = formatear_post_gratuito(chollo)
        enviar_alerta_telegram(CANAL_FREE, post_free)
    registrar_alerta_enviada(id_sub, chollo["titulo"], chollo["precio_salida_formato"])

    caption = (
        f"🚨 *Piso judicial en {chollo['localidad']} (-{chollo['ahorro_porcentaje']}% ahorro)*\n\n"
        f"📋 *Copia este texto en TikTok/Instagram:*\n"
        f"🚨 Oportunidad judicial en {chollo['localidad']} con un {chollo['ahorro_porcentaje']}% de descuento.\n"
        f"Ficha técnica, cargas y enlace oficial en el link de la bio 👆\n"
        f"#subastas #boe #inversion #madrid #chollos"
    )
    enviar_video_al_admin(ruta_video, caption)
    limpiar_temporales_render()

async def ciclo_ayudas():
    print("\n" + "="*50 + "\n💰 [VERTICAL 2] AYUDAS Y SUBVENCIONES BDNS\n" + "="*50)
    convs = obtener_convocatorias_recientes(1)
    mejores = filtrar_mejores_ayudas(convs, 1)
    if not mejores:
        print("⚠️ No hay ayudas relevantes hoy.")
        return
    ayuda = mejores[0]
    id_ayuda = ayuda["id_convocatoria"]
    ruta_video = OUTPUT_DIR / f"ayuda_{id_ayuda}_FINAL.mp4"

    await generar_video_ayuda_visual(ayuda, ruta_video)

    post = formatear_post_ayuda_vip(ayuda)
    canal_ayudas = os.getenv("TELEGRAM_CANAL_AYUDAS_ID", CANAL_VIP)
    enviar_alerta_telegram(canal_ayudas, post)
    if CANAL_FREE:
        post_free = formatear_post_ayuda_gratuito(ayuda)
        enviar_alerta_telegram(CANAL_FREE, post_free)
    registrar_alerta_enviada(id_ayuda, ayuda["titulo"], ayuda["presupuesto_formato"])

    caption = (
        f"💰 *Nueva Ayuda Oficial ({ayuda['presupuesto_formato']} a fondo perdido)*\n\n"
        f"📋 *Copia este texto en TikTok/Instagram:*\n"
        f"💰 Nueva ayuda pública de {ayuda['presupuesto_formato']} a fondo perdido para {ayuda['beneficiarios'].lower()[:40]}.\n"
        f"Plazo abierto y enlace a la sede electrónica oficial en el link del perfil 👆\n"
        f"#ayudas #subvenciones #autonomos #pymes #negocios"
    )
    enviar_video_al_admin(ruta_video, caption)
    limpiar_temporales_render()

async def ciclo_licitaciones_y_empleo():
    print("\n" + "="*50 + "\n📑 [VERTICAL 3 y 4] LICITACIONES Y EMPLEO BOE\n" + "="*50)
    lics = obtener_licitaciones_recientes()
    if lics:
        lic = lics[0]
        post_lic = formatear_post_licitacion_vip(lic)
        canal_lic = os.getenv("TELEGRAM_CANAL_LICITACIONES_ID", CANAL_VIP)
        enviar_alerta_telegram(canal_lic, post_lic)
        if CANAL_FREE:
            post_free = formatear_post_licitacion_gratuito(lic)
            enviar_alerta_telegram(CANAL_FREE, post_free)

        # Generar vídeo para Licitaciones
        id_lic = lic.get("id_licitacion", "lic").replace("-", "_")
        ruta_video_lic = OUTPUT_DIR / f"licitacion_{id_lic}_FINAL.mp4"
        await generar_video_licitacion_visual(lic, ruta_video_lic)
        cap_lic = (
            f"💼 *Contrato del Estado ({lic.get('organismo', 'Administración')[:35]})*\n\n"
            f"📋 *Copia este texto en TikTok/Instagram:*\n"
            f"💼 Nueva licitación pública en el BOE para autónomos y pymes.\n"
            f"Descarga el pliego técnico oficial en el link del perfil 👆\n"
            f"#licitaciones #autonomos #pymes #contratos #boe"
        )
        enviar_video_al_admin(ruta_video_lic, cap_lic)
        limpiar_temporales_render()

    empleos = obtener_empleo_publico_reciente()
    if empleos:
        em = empleos[0]
        post_em = formatear_post_empleo_vip(em)
        canal_em = os.getenv("TELEGRAM_CANAL_EMPLEO_ID", CANAL_VIP)
        enviar_alerta_telegram(canal_em, post_em)
        if CANAL_FREE:
            post_free = formatear_post_empleo_gratuito(em)
            enviar_alerta_telegram(CANAL_FREE, post_free)

async def ciclo_vehiculos():
    print("\n" + "="*50 + "\n🚗 [VERTICAL 5] VEHÍCULOS Y COCHES EMBARGADOS (BOE)\n" + "="*50)
    ids = buscar_subastas_vehiculos(limite=15)
    if not ids:
        print("⚠️ No hay subastas de vehículos nuevas.")
        return
    mejores = filtrar_mejores_vehiculos(ids, max_resultados=1)
    if not mejores:
        return
    v = mejores[0]
    id_sub = v["id_subasta"]

    ruta_video = OUTPUT_DIR / f"{id_sub}_VEHICULO_FINAL.mp4"
    await generar_video_vehiculo_visual(v, ruta_video)

    canal_veh = os.getenv("TELEGRAM_CANAL_VEHICULOS_ID", "-1004491031420")
    post_vip = formatear_post_vehiculo_vip(v)
    enviar_alerta_telegram(canal_veh, post_vip)

    if CANAL_FREE:
        post_free = formatear_post_vehiculo_gratuito(v)
        enviar_alerta_telegram(CANAL_FREE, post_free)

    registrar_alerta_enviada(id_sub, v["titulo"], v["precio_salida_formato"])

    caption = (
        f"🚗 *Vehículo en Subasta Pública ({v['titulo']})*\n\n"
        f"📋 *Copia este texto en TikTok/Instagram:*\n"
        f"🚨 Coche embargado en subasta oficial del BOE. Salida desde {v['precio_salida_formato']} (ahorro del -{v['ahorro_porcentaje']}%).\n"
        f"Ficha oficial, matrícula y detalles de inspección en el link de la bio 👆\n"
        f"#coches #subastas #embargos #chollos #boe"
    )
    enviar_video_al_admin(ruta_video, caption)
    limpiar_temporales_render()

async def main():
    inicializar_bd()
    purgar_archivos_antiguos(dias=3)
    hora = datetime.datetime.now().hour
    print(f"⏰ Hora del sistema: {hora}:00")

    # Selección horaria según la hora de ejecución
    if hora < 12:
        # Mañana: Subastas de Inmuebles y Vehículos
        await ciclo_subastas()
        await ciclo_vehiculos()
    elif 12 <= hora < 17:
        # Mediodía: Ayudas y Subvenciones
        await ciclo_ayudas()
    else:
        # Tarde: Licitaciones y Empleo
        await ciclo_licitaciones_y_empleo()

if __name__ == "__main__":
    purgar_archivos_antiguos(dias=3)
    if len(sys.argv) > 1:
        modo = sys.argv[1].lower()
        if modo == "subastas":
            asyncio.run(ciclo_subastas())
        elif modo == "vehiculos":
            asyncio.run(ciclo_vehiculos())
        elif modo == "ayudas":
            asyncio.run(ciclo_ayudas())
        elif modo == "licitaciones":
            asyncio.run(ciclo_licitaciones_y_empleo())
        elif modo == "urgencia":
            from src.radar_urgencia import emitir_alerta_urgencia
            emitir_alerta_urgencia()
        elif modo == "todas":
            asyncio.run(ciclo_subastas())
            asyncio.run(ciclo_vehiculos())
            asyncio.run(ciclo_ayudas())
            asyncio.run(ciclo_licitaciones_y_empleo())
            from src.radar_urgencia import emitir_alerta_urgencia
            emitir_alerta_urgencia()
    else:
        asyncio.run(main())
