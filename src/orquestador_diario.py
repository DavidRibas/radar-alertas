"""
Orquestador Diario Automatizado de RadarAlertas:
1. Extrae los chollos del día en el BOE.
2. Genera el vídeo vertical de TikTok con el motor cinematográfico.
3. Prepara y publica las alertas en Telegram (VIP y Free).
Coste: 0,00 €.
"""
import asyncio
import sys
from pathlib import Path

# Añadir raíz al PYTHONPATH
BASE_ROOT = Path(__file__).resolve().parent.parent
if str(BASE_ROOT) not in sys.path:
    sys.path.insert(0, str(BASE_ROOT))

from src.extractores.boe_inmuebles import buscar_subastas_inmuebles, filtrar_mejores_chollos
from src.telegram_bot.database import inicializar_bd, ya_fue_enviada, registrar_alerta_enviada
from src.telegram_bot.formateador import formatear_post_vip, formatear_post_gratuito
from src.video_generator.generador_visual_earth import (
    preparar_escena_1_satelite,
    preparar_escena_2_fachada,
    preparar_escena_3_interior,
    preparar_escena_4_telegram,
    generar_locucion_y_subtitulos,
    convertir_srt_a_ass,
    ensamblar_video_cinematico,
    OUTPUT_DIR
)

async def ejecutar_ciclo_diario(provincia: str = "28"):
    print("=" * 60)
    print("🚀 INICIANDO CICLO DIARIO AUTOMATIZADO DE RADARALERTAS")
    print("=" * 60)

    inicializar_bd()

    # 1. Extracción de subastas activas
    print("\n[Paso 1/3] Extrayendo convocatorias del BOE...")
    ids = buscar_subastas_inmuebles(provincia_cod=provincia, limite=20)
    if not ids:
        print("⚠️ No se encontraron subastas activas.")
        return

    mejores = filtrar_mejores_chollos(ids, max_resultados=1)
    if not mejores:
        print("⚠️ Ninguna subasta superó el filtro de calidad hoy.")
        return

    chollo = mejores[0]
    id_sub = chollo["id_subasta"]
    print(f"\n🎯 Subasta seleccionada del día: {id_sub}")
    print(f"   Ubicación: {chollo['direccion']}")
    print(f"   Valor Oficial: {chollo['valor_referencia_formato']} -> Salida: {chollo['precio_salida_formato']} (-{chollo['ahorro_porcentaje']}%)")

    # 2. Generación del Vídeo Vertical para TikTok / Reels
    print("\n[Paso 2/3] Generando vídeo cinematográfico automatizado...")
    
    e1 = OUTPUT_DIR / f"{id_sub}_e1.png"
    e2 = OUTPUT_DIR / f"{id_sub}_e2.png"
    e3 = OUTPUT_DIR / f"{id_sub}_e3.png"
    e4 = OUTPUT_DIR / f"{id_sub}_e4.png"

    preparar_escena_1_satelite(e1)
    preparar_escena_2_fachada(e2)
    preparar_escena_3_interior(e3)
    preparar_escena_4_telegram(e4)

    ruta_audio = OUTPUT_DIR / f"{id_sub}_audio.mp3"
    ruta_srt = OUTPUT_DIR / f"{id_sub}_sub.srt"
    ruta_ass = OUTPUT_DIR / f"{id_sub}_sub.ass"
    ruta_video = OUTPUT_DIR / f"{id_sub}_TIKTOK_FINAL.mp4"

    guion_dinamico = (
        f"Mira lo que acaba de publicar el BOE para {chollo['localidad']}. "
        f"Sale a subasta este inmueble tasado en {chollo['valor_referencia_formato']} "
        f"por tan solo {chollo['precio_salida_formato']}. "
        f"Es un ahorro del {chollo['ahorro_porcentaje']} por ciento respecto a su valor real. "
        "El expediente no presenta cargas hipotecarias preferentes. "
        "Tienes el enlace judicial directo y el expediente completo en nuestro canal de Telegram. "
        "Entra en el enlace de nuestro perfil."
    )

    await generar_locucion_y_subtitulos(guion_dinamico, ruta_audio, ruta_srt)
    convertir_srt_a_ass(ruta_srt, ruta_ass)

    duraciones = [3.5, 5.0, 6.5, 7.0]
    ensamblar_video_cinematico([e1, e2, e3, e4], duraciones, ruta_audio, ruta_ass, ruta_video)

    # 3. Formateo y publicación de los mensajes para Telegram
    print("\n[Paso 3/3] Formateando y enviando alertas de Telegram...")
    post_vip = formatear_post_vip(chollo)
    post_free = formatear_post_gratuito(chollo)

    # Publicar automáticamente en el Canal VIP si está configurado
    import os
    import requests
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    canal_vip = os.getenv("TELEGRAM_CANAL_VIP_ID")
    if token and canal_vip and canal_vip != "@canal_vip_demo":
        try:
            url_msg = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url_msg, json={"chat_id": canal_vip, "text": post_vip, "parse_mode": "Markdown"})
            print(f"✈️ ¡Alerta VIP enviada en directo a tu canal de Telegram ({canal_vip})!")
        except Exception as e:
            print(f"⚠️ No se pudo enviar el mensaje a Telegram: {e}")

    registrar_alerta_enviada(id_sub, chollo["titulo"], chollo["precio_salida_formato"])

    print("\n" + "=" * 60)
    print("✅ CICLO COMPLETADO CON ÉXITO")
    print("=" * 60)
    print(f"🎬 Vídeo listo para TikTok: {ruta_video}")
    print("\n📩 Post generado para Canal VIP de Telegram:\n" + post_vip)
    print("-" * 60)
    print("📢 Post teaser para Canal Gratuito de Telegram:\n" + post_free)

if __name__ == "__main__":
    asyncio.run(ejecutar_ciclo_diario(provincia="28"))
