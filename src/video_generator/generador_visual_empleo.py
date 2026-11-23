"""
Generador de Vídeos Verticales ULTRA-VISUALES para Empleo Público y Oposiciones (BOE Sección 2B).
Estética cinematográfica 9:16 para TikTok y Reels con tipografía gigante,
notificación de nómina fija del Estado, fotos reales y ganchos visuales irresistibles.
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

def crear_escena_empleo_1_nomina(em: dict, ruta_salida: Path):
    """Escena 1: Gancho ultra-visual de nómina fija del Estado con sueldo gigante."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "empleo_oficial_estado.jpg", ancho, alto, oscurecer=120)
    draw = ImageDraw.Draw(img)

    # 1. Badge superior de Alerta
    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(220, 38, 38))
    texto_centrado_auto(draw, "🚨 CONVOCATORIA DE EMPLEO BOE", badge_rect, "arialbd.ttf", 40, (255, 255, 255))

    # 2. Tarjeta Central tipo Nómina / Sueldo Público
    noti_rect = [80, 620, 1000, 1060]
    draw.rounded_rectangle(noti_rect, radius=32, fill=(15, 23, 42), outline=(245, 158, 11), width=5)

    draw.text((540, 675), "🏛️ RETRIBUCIÓN PÚBLICA OFICIAL", font=ImageFont.truetype("arialbd.ttf", 30), fill=(254, 243, 199), anchor="mm")
    draw.text((540, 775), "+2.150 € / MES", font=ImageFont.truetype("arialbd.ttf", 82), fill=(34, 197, 94), anchor="mm")
    draw.text((540, 870), "14 PAGAS + EMPLEO PARA TODA LA VIDA", font=ImageFont.truetype("arialbd.ttf", 34), fill=(241, 245, 249), anchor="mm")

    sello_rect = [130, 930, 950, 1020]
    draw.rounded_rectangle(sello_rect, radius=20, fill=(20, 83, 45), outline=(34, 197, 94), width=3)
    draw.text((540, 975), "✅ BOLSAS DE EMPLEO Y PLAZAS FIJAS", font=ImageFont.truetype("arialbd.ttf", 34), fill=(187, 247, 208), anchor="mm")

    # 3. Píldora inferior del Organismo
    org = em.get("organismo", "ADMINISTRACIÓN GENERAL DEL ESTADO")[:50]
    sub_rect = [100, 1220, 980, 1340]
    draw.rounded_rectangle(sub_rect, radius=22, fill=(30, 41, 59), outline=(148, 163, 184), width=2)
    texto_centrado_auto(draw, f"🏛️ {org.upper()}", sub_rect, "arialbd.ttf", 34, (255, 255, 255))

    img.save(ruta_salida, quality=95)

def crear_escena_empleo_2_requisitos(em: dict, ruta_salida: Path):
    """Escena 2: Requisitos mínimos ultra claros y directos."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "ayuda_autonomo_trabajando.jpg", ancho, alto, oscurecer=130)
    draw = ImageDraw.Draw(img)

    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(180, 83, 9))
    texto_centrado_auto(draw, "🎯 REQUISITOS DE ACCESO", badge_rect, "arialbd.ttf", 40, (255, 255, 255))

    card_rect = [80, 580, 1000, 1160]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(245, 158, 11), width=5)

    checks = [
        ("✅ TITULACIÓN BÁSICA SEGÚN BASES", "Desde ESO o Bachillerato hasta Grado"),
        ("✅ SIN EXAMEN DURO (BOLSA O MÉRITOS)", "Procesos rápidos de incorporación"),
        ("✅ CONVOCATORIA OFICIAL PUBLICADA", "Plazas reguladas hoy en el BOE")
    ]
    y_pos = 650
    for tit, sub in checks:
        draw.text((120, y_pos), tit, font=ImageFont.truetype("arialbd.ttf", 36), fill=(251, 191, 36))
        draw.text((120, y_pos + 46), sub, font=ImageFont.truetype("arial.ttf", 30), fill=(226, 232, 240))
        y_pos += 120

    sello_rect = [120, 1030, 960, 1120]
    draw.rounded_rectangle(sello_rect, radius=20, fill=(30, 58, 138), outline=(96, 165, 250), width=2)
    draw.text((540, 1075), "⚡ PLAZAS EN TODA ESPAÑA", font=ImageFont.truetype("arialbd.ttf", 32), fill=(219, 234, 254), anchor="mm")

    img.save(ruta_salida, quality=95)

def crear_escena_empleo_3_plazo(em: dict, ruta_salida: Path):
    """Escena 3: Reloj de urgencia y llamada a la instancia oficial."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "empleo_oficial_estado.jpg", ancho, alto, oscurecer=130)
    draw = ImageDraw.Draw(img)

    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(234, 179, 8))
    texto_centrado_auto(draw, "⏳ PLAZO DE SOLICITUD ABIERTO", badge_rect, "arialbd.ttf", 38, (15, 23, 42))

    card_rect = [80, 600, 1000, 1140]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(234, 179, 8), width=5)

    draw.text((540, 680), "PUBLICADO EN BOE SECCIÓN 2B", font=ImageFont.truetype("arialbd.ttf", 34), fill=(148, 163, 184), anchor="mm")
    draw.text((540, 780), "CONVOCATORIA ACTIVA", font=ImageFont.truetype("arialbd.ttf", 52), fill=(248, 250, 252), anchor="mm")
    draw.text((540, 870), f"ID: {em.get('id_convocatoria', 'BOE-2B')}", font=ImageFont.truetype("arialbd.ttf", 44), fill=(250, 204, 21), anchor="mm")

    box_btn = [120, 970, 960, 1080]
    draw.rounded_rectangle(box_btn, radius=20, fill=(185, 28, 28))
    draw.text((540, 1025), "🚨 20 DÍAS HÁBILES PARA INSCRIPCIÓN", font=ImageFont.truetype("arialbd.ttf", 32), fill=(255, 255, 255), anchor="mm")

    img.save(ruta_salida, quality=95)

def crear_escena_empleo_4_cta(ruta_salida: Path):
    """Escena 4: Pantalla final de RadarAlertas Telegram."""
    ancho, alto = 1080, 1920
    img = Image.new("RGB", (ancho, alto), (11, 15, 25))
    draw = ImageDraw.Draw(img)

    banner_rect = [80, 320, 1000, 440]
    draw.rounded_rectangle(banner_rect, radius=24, fill=(220, 38, 38))
    texto_centrado_auto(draw, "💼 RADARALERTAS TELEGRAM", banner_rect, "arialbd.ttf", 42, (255, 255, 255))

    card_rect = [80, 520, 1000, 1340]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(220, 38, 38), width=4)

    draw.text((540, 600), "📲 BASES Y FORMULARIO OFICIAL", font=ImageFont.truetype("arialbd.ttf", 38), fill=(251, 191, 36), anchor="mm")

    beneficios = [
        "✅ Descarga del PDF oficial del BOE",
        "✅ Enlace directo al formulario de solicitud",
        "✅ Requisitos y temario simplificado",
        "✅ Avisos al instante de nuevas plazas fijas"
    ]
    y_b = 700
    for b in beneficios:
        draw.text((140, y_b), b, font=ImageFont.truetype("arial.ttf", 32), fill=(248, 250, 252))
        y_b += 95

    btn_rect = [100, 1130, 980, 1270]
    draw.rounded_rectangle(btn_rect, radius=24, fill=(37, 99, 235))
    draw.text((540, 1175), "👉 WEB EN DESCRIPCIÓN DEL PERFIL", font=ImageFont.truetype("arialbd.ttf", 40), fill=(255, 255, 255), anchor="mm")
    draw.text((540, 1225), "Web: radaralertas.com", font=ImageFont.truetype("arial.ttf", 26), fill=(219, 234, 254), anchor="mm")

    img.save(ruta_salida, quality=95)

async def generar_locucion_empleo(em: dict, ruta_mp3: Path, ruta_srt: Path):
    """Genera la locución con Edge-TTS."""
    org = em.get("organismo", "el Estado")[:40]
    tit = em.get("titulo", "plazas de empleo público").replace("Resolución de ", "")[:65]

    guion = (
        f"Atención si buscas un sueldo fijo y empleo para toda la vida. "
        f"El Boletín Oficial del Estado acaba de publicar una nueva convocatoria pública. "
        f"Convocada por {org} para {tit}. "
        f"Con sueldo oficial, catorce pagas y requisitos abiertos de acceso. "
        f"El documento oficial en PDF con las bases y el enlace directo están en nuestra web oficial. "
        f"Entra a la web que tienes en la descripción de nuestro perfil para ver todos los detalles."
    )

    comunicador = edge_tts.Communicate(guion, voice="es-ES-AlvaroNeural", rate="+6%")
    sub_maker = edge_tts.SubMaker()
    with open(ruta_mp3, "wb") as f_mp3:
        async for chunk in comunicador.stream():
            if chunk["type"] == "audio":
                f_mp3.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                sub_maker.feed(chunk)

    with open(ruta_srt, "w", encoding="utf-8") as f_srt:
        f_srt.write(sub_maker.get_srt())

async def generar_video_empleo_visual(em: dict, ruta_salida_mp4: Path):
    """Genera el vídeo ultra-visual de Empleo en formato vertical 9:16."""
    id_emp = em.get("id_convocatoria", "emp").replace("-", "_")
    e1 = OUTPUT_DIR / f"emp_{id_emp}_e1.png"
    e2 = OUTPUT_DIR / f"emp_{id_emp}_e2.png"
    e3 = OUTPUT_DIR / f"emp_{id_emp}_e3.png"
    e4 = OUTPUT_DIR / f"emp_{id_emp}_e4.png"

    crear_escena_empleo_1_nomina(em, e1)
    crear_escena_empleo_2_requisitos(em, e2)
    crear_escena_empleo_3_plazo(em, e3)
    crear_escena_empleo_4_cta(e4)

    ruta_audio = OUTPUT_DIR / f"emp_{id_emp}_audio.mp3"
    ruta_srt = OUTPUT_DIR / f"emp_{id_emp}_sub.srt"
    ruta_ass = OUTPUT_DIR / f"emp_{id_emp}_sub.ass"

    await generar_locucion_empleo(em, ruta_audio, ruta_srt)
    convertir_srt_a_ass(ruta_srt, ruta_ass)

    dur_audio = obtener_duracion_audio(ruta_audio)
    d1 = 5.0
    d2 = 5.0
    d3 = 5.0
    d4 = max(4.0, (dur_audio - 15.0) + 2.0)

    ensamblar_video_cinematico(
        [e1, e2, e3, e4],
        [d1, d2, d3, d4],
        ruta_audio,
        ruta_ass,
        ruta_salida_mp4
    )
    print(f"🎬 [Vídeo Empleo ULTRA-VISUAL] Generado: {ruta_salida_mp4.name} ({dur_audio:.1f}s)")
