"""
Generador de Vídeos Verticales ULTRA-VISUALES para Vehículos y Coches Embargados (BOE).
Estética cinematográfica 9:16 para TikTok y Reels con ganchos visuales potentes,
precios de salida ridículos, marcas reconocidas y llamadas a la acción irresistibles.
"""
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"
OUTPUT_DIR.mkdir(exist_ok=True)

from src.video_generator.generador_visual_earth import (
    obtener_ruta_ffmpeg,
    obtener_duracion_audio,
    texto_centrado_auto,
    convertir_srt_a_ass,
    ensamblar_video_cinematico
)
from src.video_generator.generador_visual_ayudas import preparar_fondo_con_overlay

def crear_escena_vehiculo_1_coche(vehiculo: dict, ruta_salida: Path):
    """Escena 1: Gancho ultra-visual con foto de coche, modelo y precio de salida ridículo."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "vehiculo_coche_oficial.jpg", ancho, alto, oscurecer=110)
    draw = ImageDraw.Draw(img)

    # 1. Badge superior de Alerta
    badge_rect = [80, 200, 1000, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(220, 38, 38))
    texto_centrado_auto(draw, "🚨 VEHÍCULOS EMBARGADOS POR EL ESTADO", badge_rect, "arialbd.ttf", 38, (255, 255, 255))

    # 2. Tarjeta Central tipo Notificación Oficial
    noti_rect = [70, 600, 1010, 1080]
    draw.rounded_rectangle(noti_rect, radius=32, fill=(15, 23, 42), outline=(234, 179, 8), width=5)

    draw.text((540, 660), "🏛️ SUBASTA PÚBLICA OFICIAL (BOE)", font=ImageFont.truetype("arialbd.ttf", 30), fill=(250, 204, 21), anchor="mm")

    tit = vehiculo.get("titulo", "VEHÍCULO EN SUBASTA")[:26].upper()
    draw.text((540, 750), tit, font=ImageFont.truetype("arialbd.ttf", 64), fill=(255, 255, 255), anchor="mm")

    salida_txt = f"SALIDA: {vehiculo.get('precio_salida_formato', '980 €')}"
    draw.text((540, 850), salida_txt, font=ImageFont.truetype("arialbd.ttf", 74), fill=(34, 197, 94), anchor="mm")

    tasacion = vehiculo.get("valor_referencia_formato", "2.000 €")
    ahorro = vehiculo.get("ahorro_porcentaje", 50)
    sub_txt = f"TASACIÓN: {tasacion} • AHORRO DEL -{ahorro}%"
    draw.text((540, 930), sub_txt, font=ImageFont.truetype("arialbd.ttf", 30), fill=(203, 213, 225), anchor="mm")

    sello_rect = [120, 970, 960, 1050]
    draw.rounded_rectangle(sello_rect, radius=18, fill=(20, 83, 45), outline=(34, 197, 94), width=3)
    draw.text((540, 1010), "✅ SIN CARGAS Y CON REVISIÓN PREVIA", font=ImageFont.truetype("arialbd.ttf", 32), fill=(187, 247, 208), anchor="mm")

    # 3. Píldora inferior de Ubicación
    prov = vehiculo.get("provincia", "ESPAÑA").upper()
    loc_rect = [100, 1220, 980, 1330]
    draw.rounded_rectangle(loc_rect, radius=22, fill=(30, 41, 59), outline=(148, 163, 184), width=2)
    texto_centrado_auto(draw, f"📍 {prov} • DEPÓSITO JUDICIAL OFICIAL", loc_rect, "arialbd.ttf", 34, (255, 255, 255))

    img.save(ruta_salida, quality=95)

def crear_escena_vehiculo_2_ventajas(vehiculo: dict, ruta_salida: Path):
    """Escena 2: Foto de llaves con 3 ventajas contundentes."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "vehiculo_llaves_concesionario.jpg", ancho, alto, oscurecer=125)
    draw = ImageDraw.Draw(img)

    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(37, 99, 235))
    texto_centrado_auto(draw, "🎯 ¿CÓMO FUNCIONA LA SUBASTA?", badge_rect, "arialbd.ttf", 40, (255, 255, 255))

    card_rect = [80, 580, 1000, 1160]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(59, 130, 246), width=5)

    checks = [
        ("🚗 COCHES, SUVS Y FURGONETAS", "Precios fijados por Juzgados y Ayuntamientos"),
        ("🔍 INSPECCIÓN MECÁNICA PREVIA", "Visita con cita previa antes de pujar"),
        ("📱 PUJA 100% ONLINE EN EL BOE", "Sin intermediarios ni comisiones abusivas")
    ]
    y_pos = 650
    for tit, sub in checks:
        draw.text((120, y_pos), tit, font=ImageFont.truetype("arialbd.ttf", 36), fill=(251, 191, 36))
        draw.text((120, y_pos + 46), sub, font=ImageFont.truetype("arial.ttf", 30), fill=(226, 232, 240))
        y_pos += 120

    sello_rect = [120, 1030, 960, 1120]
    draw.rounded_rectangle(sello_rect, radius=20, fill=(30, 58, 138), outline=(96, 165, 250), width=2)
    draw.text((540, 1075), "⚡ ACCESO PÚBLICO Y DIRECTO", font=ImageFont.truetype("arialbd.ttf", 32), fill=(219, 234, 254), anchor="mm")

    img.save(ruta_salida, quality=95)

def crear_escena_vehiculo_3_expediente(vehiculo: dict, ruta_salida: Path):
    """Escena 3: Expediente oficial, matrícula auditada y llamada a la acción."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "vehiculo_coche_oficial.jpg", ancho, alto, oscurecer=130)
    draw = ImageDraw.Draw(img)

    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(234, 179, 8))
    texto_centrado_auto(draw, "⏳ SUBASTA ABIERTA - PLAZO ACTIVO", badge_rect, "arialbd.ttf", 38, (15, 23, 42))

    card_rect = [80, 600, 1000, 1140]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(234, 179, 8), width=5)

    id_sub = vehiculo.get("id_subasta", "BOE-VEHICULOS")
    draw.text((540, 660), f"EXPEDIENTE: {id_sub}", font=ImageFont.truetype("arialbd.ttf", 30), fill=(148, 163, 184), anchor="mm")

    mat = vehiculo.get("matricula", "AUDITADA")
    draw.text((540, 740), f"MATRÍCULA: {mat}", font=ImageFont.truetype("arialbd.ttf", 52), fill=(255, 255, 255), anchor="mm")

    fin = vehiculo.get("fecha_fin", "Próxima conclusión")
    draw.text((540, 830), f"CIERRE: {fin}", font=ImageFont.truetype("arialbd.ttf", 32), fill=(250, 204, 21), anchor="mm")

    btn_rect = [120, 920, 960, 1060]
    draw.rounded_rectangle(btn_rect, radius=24, fill=(220, 38, 38))
    texto_centrado_auto(draw, "🚨 DESCARGA EL LISTADO COMPLETO", btn_rect, "arialbd.ttf", 36, (255, 255, 255))

    sub_rect = [100, 1220, 980, 1340]
    draw.rounded_rectangle(sub_rect, radius=22, fill=(30, 41, 59), outline=(148, 163, 184), width=2)
    texto_centrado_auto(draw, "👉 ENLACE AL EXPEDIENTE EN LA BIO", sub_rect, "arialbd.ttf", 36, (255, 255, 255))

    img.save(ruta_salida, quality=95)

def crear_escena_vehiculo_4_telegram(vehiculo: dict, ruta_salida: Path):
    """Escena 4: Tarjeta Telegram RadarAlertas VIP."""
    ancho, alto = 1080, 1920
    img = Image.new("RGB", (ancho, alto), (10, 15, 29))
    draw = ImageDraw.Draw(img)

    for y in range(alto):
        r = int(10 + (25 - 10) * (y / alto))
        g = int(15 + (35 - 15) * (y / alto))
        b = int(29 + (55 - 29) * (y / alto))
        draw.line([(0, y), (ancho, y)], fill=(r, g, b))

    card_rect = [100, 500, 980, 1350]
    draw.rounded_rectangle(card_rect, radius=36, fill=(15, 23, 42), outline=(59, 130, 246), width=4)

    draw.text((540, 600), "📱 RADARALERTAS VIP", font=ImageFont.truetype("arialbd.ttf", 46), fill=(255, 255, 255), anchor="mm")
    draw.text((540, 670), "CANAL EXCLUSIVO DE VEHÍCULOS", font=ImageFont.truetype("arialbd.ttf", 32), fill=(147, 197, 253), anchor="mm")

    features = [
        "🚗 Fotos, matrícula y número de bastidor",
        "🔍 Cita previa para revisión mecánica",
        "⚖️ Informe de multas y precintos",
        "🔗 Enlace directo a la puja en el BOE"
    ]
    y_feat = 780
    for feat in features:
        draw.text((150, y_feat), feat, font=ImageFont.truetype("arial.ttf", 32), fill=(226, 232, 240))
        y_feat += 85

    btn_rect = [160, 1170, 920, 1270]
    draw.rounded_rectangle(btn_rect, radius=28, fill=(37, 99, 235))
    texto_centrado_auto(draw, "👉 TOCA EL LINK DE LA BIO", btn_rect, "arialbd.ttf", 38, (255, 255, 255))

    img.save(ruta_salida, quality=95)

async def generar_locucion_vehiculo(vehiculo: dict, ruta_audio: Path, ruta_srt: Path):
    """Genera la locución con Edge-TTS para el vídeo de vehículos."""
    tit = vehiculo.get("titulo", "este vehículo")
    prov = vehiculo.get("provincia", "España")
    salida = vehiculo.get("precio_salida_formato", "menos de mil euros")
    tasacion = vehiculo.get("valor_referencia_formato", "su tasación de mercado")
    ahorro = vehiculo.get("ahorro_porcentaje", 50)

    guion = (
        f"Atención a esta oportunidad en el Boletín Oficial del Estado. "
        f"Acaba de salir a subasta pública este {tit} en {prov}, "
        f"con un precio de salida de tan solo {salida}, frente a una tasación de {tasacion}, "
        f"lo que supone un ahorro del {ahorro} por ciento. "
        f"El vehículo cuenta con expediente oficial, matrícula auditada y la posibilidad de solicitar inspección previa en el depósito municipal. "
        f"Puedes participar de forma 100% telemática con certificado digital o DNI electrónico. "
        f"Tienes todos los detalles, matrícula y el enlace oficial al expediente en el link de nuestra biografía."
    )

    com = edge_tts.Communicate(guion, voice="es-ES-AlvaroNeural", rate="+15%")
    submaker = edge_tts.SubMaker()
    with open(ruta_audio, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)

    with open(ruta_srt, "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())

async def generar_video_vehiculo_visual(vehiculo: dict, ruta_final: Path):
    """Genera el vídeo ultra-visual completo de vehículos."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    e1 = OUTPUT_DIR / "temp_vehiculo_1.png"
    e2 = OUTPUT_DIR / "temp_vehiculo_2.png"
    e3 = OUTPUT_DIR / "temp_vehiculo_3.png"
    e4 = OUTPUT_DIR / "temp_vehiculo_4.png"

    crear_escena_vehiculo_1_coche(vehiculo, e1)
    crear_escena_vehiculo_2_ventajas(vehiculo, e2)
    crear_escena_vehiculo_3_expediente(vehiculo, e3)
    crear_escena_vehiculo_4_telegram(vehiculo, e4)

    ruta_audio = OUTPUT_DIR / "audio_vehiculo.mp3"
    ruta_srt = OUTPUT_DIR / "subtitulos_vehiculo.srt"
    ruta_ass = OUTPUT_DIR / "subtitulos_vehiculo.ass"

    await generar_locucion_vehiculo(vehiculo, ruta_audio, ruta_srt)
    convertir_srt_a_ass(ruta_srt, ruta_ass)

    dur_total = obtener_duracion_audio(ruta_audio)
    d1 = dur_total * 0.28
    d2 = dur_total * 0.28
    d3 = dur_total * 0.24
    d4 = (dur_total * 0.20) + 2.0

    escenas = [e1, e2, e3, e4]
    duraciones = [d1, d2, d3, d4]

    ensamblar_video_cinematico(escenas, duraciones, ruta_audio, ruta_ass, ruta_final)
    print(f"🎬 [Vídeo Vehículos ULTRA-VISUAL] Generado: {ruta_final.name} ({dur_total:.1f}s)")
