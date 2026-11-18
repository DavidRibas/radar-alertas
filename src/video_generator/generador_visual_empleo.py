"""
Generador de Vídeos Verticales para Empleo Público y Oposiciones (BOE Sección 2B).
Produce vídeos dinámicos en formato 9:16 (TikTok / Reels / Shorts) con estética oficial,
locución neuronal Edge-TTS y subtítulos dinámicos sincronizados.
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

def crear_escena_empleo_1_convocatoria(em: dict, ruta_salida: Path):
    """Escena 1: Gancho visual de empleo público y plazas abiertas en el BOE."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "empleo_oficial_estado.jpg", ancho, alto, oscurecer=130)
    draw = ImageDraw.Draw(img)

    # 1. Badge superior de Alerta
    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(220, 38, 38)) # Rojo alerta urgente
    texto_centrado_auto(draw, "🚨 CONVOCATORIA DE EMPLEO BOE", badge_rect, "arialbd.ttf", 38, (255, 255, 255))

    # 2. Tarjeta Central tipo Notificación Oficial
    card_rect = [70, 360, 1010, 1260]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42, 235), outline=(245, 158, 11), width=3)

    # Sub-badge Plazas
    cat_rect = [120, 420, 960, 500]
    draw.rounded_rectangle(cat_rect, radius=18, fill=(180, 83, 9))
    texto_centrado_auto(draw, "💼 PLAZAS Y BOLSAS DE EMPLEO DEL ESTADO", cat_rect, "arialbd.ttf", 30, (254, 243, 199))

    # Organismo
    org = em.get("organismo", "ADMINISTRACIÓN DEL ESTADO").upper()
    org_lineas = [org[i:i+35] for i in range(0, min(len(org), 70), 35)]
    y_org = 540
    for linea in org_lineas:
        draw.text((120, y_org), f"🏛️ {linea}", font=ImageFont.truetype("arialbd.ttf", 32), fill=(248, 250, 252))
        y_org += 48

    # Título y plazas
    draw.text((120, 680), "📋 BASES PUBLICADAS:", font=ImageFont.truetype("arialbd.ttf", 30), fill=(251, 191, 36))
    titulo = em.get("titulo", "Convocatoria pública de plazas del Estado")
    titulo_limpio = titulo.replace("Resolución de ", "").replace("Orden de ", "")
    palabras = titulo_limpio.split()
    lineas_titulo = []
    actual = []
    for p in palabras:
        actual.append(p)
        if len(" ".join(actual)) > 36:
            lineas_titulo.append(" ".join(actual[:-1]))
            actual = [p]
    if actual:
        lineas_titulo.append(" ".join(actual))

    y_tit = 740
    for l in lineas_titulo[:4]:
        draw.text((120, y_tit), l, font=ImageFont.truetype("arial.ttf", 32), fill=(226, 232, 240))
        y_tit += 48

    # Sello de Empleo Estable
    sello_rect = [120, 1020, 960, 1160]
    draw.rounded_rectangle(sello_rect, radius=24, fill=(16, 185, 129))
    draw.text((160, 1045), "✅ ESTABILIDAD Y SUELDO FIJO", font=ImageFont.truetype("arialbd.ttf", 34), fill=(255, 255, 255))
    draw.text((160, 1100), "Publicado hoy en el Boletín Oficial del Estado", font=ImageFont.truetype("arial.ttf", 28), fill=(240, 253, 244))

    # Badge inferior de Urgencia
    urg_rect = [120, 1350, 960, 1450]
    draw.rounded_rectangle(urg_rect, radius=20, fill=(37, 99, 235))
    texto_centrado_auto(draw, "⏳ PLAZO DE INSCRIPCIÓN ABIERTO", urg_rect, "arialbd.ttf", 32, (255, 255, 255))

    img.save(ruta_salida, quality=95)

def crear_escena_empleo_2_condiciones(em: dict, ruta_salida: Path):
    """Escena 2: Requisitos de acceso y condiciones laborales."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "empleo_oficial_estado.jpg", ancho, alto, oscurecer=145)
    draw = ImageDraw.Draw(img)

    head_rect = [100, 200, 980, 290]
    draw.rounded_rectangle(head_rect, radius=20, fill=(180, 83, 9))
    texto_centrado_auto(draw, "📋 CONDICIONES Y REQUISITOS", head_rect, "arialbd.ttf", 36, (255, 255, 255))

    card_rect = [80, 360, 1000, 1320]
    draw.rounded_rectangle(card_rect, radius=30, fill=(15, 23, 42, 235), outline=(245, 158, 11), width=2)

    items = [
        ("🎓 Titulación requerida:", "Ver bases oficiales según grupo profesional."),
        ("💶 Retribución orientativa:", "Sueldo oficial regulado por tablas del Estado."),
        ("📅 Calendario de solicitudes:", "Plazo oficial de 20 días hábiles desde publicación."),
        ("📥 Dónde descargar el temario y bases:", "Disponible enlace al PDF oficial en RadarAlertas.")
    ]

    y_pos = 430
    for tit, desc in items:
        draw.text((130, y_pos), tit, font=ImageFont.truetype("arialbd.ttf", 32), fill=(251, 191, 36))
        y_pos += 46
        draw.text((130, y_pos), desc, font=ImageFont.truetype("arial.ttf", 28), fill=(226, 232, 240))
        y_pos += 80

    call_rect = [120, 1150, 960, 1260]
    draw.rounded_rectangle(call_rect, radius=20, fill=(16, 185, 129))
    texto_centrado_auto(draw, "🎯 OPORTUNIDAD REAL DE EMPLEO PÚBLICO", call_rect, "arialbd.ttf", 32, (255, 255, 255))

    img.save(ruta_salida, quality=95)

def crear_escena_empleo_3_cta(ruta_salida: Path):
    """Escena 3: Pantalla de llamada a la acción hacia el canal de Telegram."""
    ancho, alto = 1080, 1920
    img = Image.new("RGB", (ancho, alto), (11, 15, 25))
    draw = ImageDraw.Draw(img)

    banner_rect = [80, 300, 1000, 420]
    draw.rounded_rectangle(banner_rect, radius=24, fill=(220, 38, 38))
    texto_centrado_auto(draw, "💼 RADAR DE EMPLEO DEL ESTADO", banner_rect, "arialbd.ttf", 38, (255, 255, 255))

    # Cuadro principal
    box_rect = [80, 480, 1000, 1350]
    draw.rounded_rectangle(box_rect, radius=32, fill=(15, 23, 42), outline=(245, 158, 11), width=3)

    draw.text((140, 550), "📲 BASES OFICIALES EN TELEGRAM", font=ImageFont.truetype("arialbd.ttf", 34), fill=(251, 191, 36))

    beneficios = [
        "✅ Descarga del PDF oficial del BOE con las plazas",
        "✅ Enlace directo al formulario de inscripción",
        "✅ Avisos al instante de bolsas urgentes de trabajo",
        "✅ Filtro directo de oposiciones sin examen difícil"
    ]
    y_b = 660
    for b in beneficios:
        draw.text((140, y_b), b, font=ImageFont.truetype("arial.ttf", 30), fill=(248, 250, 252))
        y_b += 95

    # Botón Telegram
    tg_btn = [120, 1120, 960, 1260]
    draw.rounded_rectangle(tg_btn, radius=28, fill=(37, 99, 235))
    draw.text((220, 1150), "👉 ENTRA AL LINK DE LA BIO", font=ImageFont.truetype("arialbd.ttf", 44), fill=(255, 255, 255))
    draw.text((290, 1205), "Canal Telegram: @radar_alertas", font=ImageFont.truetype("arial.ttf", 28), fill=(219, 234, 254))

    img.save(ruta_salida, quality=95)

async def generar_locucion_empleo(em: dict, ruta_mp3: Path, ruta_srt: Path):
    """Genera la locución con voz profesional de Edge-TTS."""
    org = em.get("organismo", "la administración pública")
    tit = em.get("titulo", "plazas de empleo del estado")
    tit_breve = tit.replace("Resolución de ", "").replace("Orden de ", "")[:90]

    guion = (
        f"Atención si estás buscando empleo fijo o estabilidad laboral. "
        f"El Boletín Oficial del Estado acaba de publicar una nueva convocatoria pública. "
        f"Es para {org}. "
        f"Se aprueban las bases para {tit_breve}. "
        f"El plazo oficial de inscripción está abierto desde hoy. "
        f"Tienes las bases completas en PDF y el formulario oficial en nuestro canal de Telegram. "
        f"Toca el enlace de nuestro perfil para acceder a la convocatoria."
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
    """Orquesta la creación de imágenes, locución, subtítulos y ensamblado cinemático del vídeo."""
    id_emp = em.get("id_convocatoria", "emp_01")
    e1 = OUTPUT_DIR / f"emp_{id_emp}_e1.png"
    e2 = OUTPUT_DIR / f"emp_{id_emp}_e2.png"
    e3 = OUTPUT_DIR / f"emp_{id_emp}_e3.png"

    crear_escena_empleo_1_convocatoria(em, e1)
    crear_escena_empleo_2_condiciones(em, e2)
    crear_escena_empleo_3_cta(e3)

    ruta_audio = OUTPUT_DIR / f"emp_{id_emp}_audio.mp3"
    ruta_srt = OUTPUT_DIR / f"emp_{id_emp}_sub.srt"
    ruta_ass = OUTPUT_DIR / f"emp_{id_emp}_sub.ass"

    await generar_locucion_empleo(em, ruta_audio, ruta_srt)
    convertir_srt_a_ass(ruta_srt, ruta_ass)

    dur_audio = obtener_duracion_audio(ruta_audio)
    d1 = 5.0
    d2 = 6.0
    d3 = max(4.0, (dur_audio - 11.0) + 2.0)

    ensamblar_video_cinematico(
        [e1, e2, e3],
        [d1, d2, d3],
        ruta_audio,
        ruta_ass,
        ruta_salida_mp4
    )
    print(f"✅ [Vídeo Empleo] Generado con éxito: {ruta_salida_mp4.name} ({dur_audio:.1f}s)")
