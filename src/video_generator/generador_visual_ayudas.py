"""
Generador de Vídeos Verticales ULTRA-VISUALES para Ayudas y Subvenciones.
Utiliza fotografía real de alta resolución, efectos de notificación bancaria,
fondos dinámicos y ganchos de alto impacto visual (TikTok / Reels).
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

def preparar_fondo_con_overlay(ruta_fondo: Path, ancho: int = 1080, alto: int = 1920, oscurecer: int = 110) -> Image.Image:
    """Abre la imagen fotográfica real, la escala verticalmente y le añade un viñeteado cinematográfico."""
    img = Image.open(ruta_fondo).convert("RGB")
    ratio = max(ancho / img.width, alto / img.height)
    nuevo_tam = (int(img.width * ratio), int(img.height * ratio))
    img = img.resize(nuevo_tam, Image.Resampling.LANCZOS)
    left = (img.width - ancho) // 2
    top = (img.height - alto) // 2
    img = img.crop((left, top, left + ancho, top + alto))

    overlay = Image.new("RGBA", (ancho, alto), (11, 15, 25, oscurecer))
    img.paste(overlay, (0, 0), overlay)
    return img

def crear_escena_ayuda_1_notificacion(ayuda: dict, ruta_salida: Path):
    """Escena 1: Gancho brutal con foto real de dinero + Notificación bancaria tipo iPhone."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "ayuda_dinero_euros.jpg", ancho, alto, oscurecer=120)
    draw = ImageDraw.Draw(img)

    # 1. Badge superior de Alerta
    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(220, 38, 38))
    texto_centrado_auto(draw, "🚨 DINERO PÚBLICO A FONDO PERDIDO", badge_rect, "arialbd.ttf", 40, (255, 255, 255))

    # 2. Notificación Bancaria Móvil (Efecto psicológico de ingreso de dinero)
    noti_rect = [80, 680, 1000, 1040]
    draw.rounded_rectangle(noti_rect, radius=32, fill=(15, 23, 42), outline=(34, 197, 94), width=5)

    draw.text((120, 725), "📱 BANCA MÓVIL • INGRESO CONFIRMADO", font=ImageFont.truetype("arialbd.ttf", 32), fill=(148, 163, 184))
    draw.text((540, 830), f"+{ayuda['presupuesto_formato']}", font=ImageFont.truetype("arialbd.ttf", 92), fill=(34, 197, 94), anchor="mm")
    draw.text((540, 930), "CONCEPTO: SUBVENCIÓN DIRECTA BOE", font=ImageFont.truetype("arialbd.ttf", 34), fill=(226, 232, 240), anchor="mm")
    draw.text((540, 985), "ESTADO: NO REQUIERE DEVOLUCIÓN", font=ImageFont.truetype("arialbd.ttf", 30), fill=(250, 204, 21), anchor="mm")

    # 3. Píldora inferior de la ayuda concreta
    sub_rect = [100, 1220, 980, 1340]
    draw.rounded_rectangle(sub_rect, radius=22, fill=(30, 41, 59), outline=(148, 163, 184), width=2)
    texto_centrado_auto(draw, ayuda["titulo"].upper()[:65], sub_rect, "arialbd.ttf", 36, (255, 255, 255))

    img.save(ruta_salida, quality=95)

def crear_escena_ayuda_2_beneficiarios(ayuda: dict, ruta_salida: Path):
    """Escena 2: Foto real de comercio/tienda con requisitos ultra claros."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "ayuda_comercio_real.jpg", ancho, alto, oscurecer=130)
    draw = ImageDraw.Draw(img)

    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(59, 130, 246))
    texto_centrado_auto(draw, "🎯 ¿QUIÉN PUEDE PEDIRLO?", badge_rect, "arialbd.ttf", 40, (255, 255, 255))

    card_rect = [80, 650, 1000, 1100]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(59, 130, 246), width=5)

    draw.text((540, 720), "DESTINATARIOS OFICIALES", font=ImageFont.truetype("arialbd.ttf", 34), fill=(148, 163, 184), anchor="mm")

    b_text_rect = [120, 770, 960, 920]
    texto_centrado_auto(draw, ayuda["beneficiarios"].upper()[:75], b_text_rect, "arialbd.ttf", 46, (255, 255, 255))

    sello_rect = [120, 960, 960, 1050]
    draw.rounded_rectangle(sello_rect, radius=20, fill=(20, 83, 45), outline=(34, 197, 94), width=3)
    draw.text((540, 1005), "✅ 100% SUBVENCIONADO (A FONDO PERDIDO)", font=ImageFont.truetype("arialbd.ttf", 32), fill=(187, 247, 208), anchor="mm")

    img.save(ruta_salida, quality=95)

def crear_escena_ayuda_3_plazo(ayuda: dict, ruta_salida: Path):
    """Escena 3: Foto real de despacho con reloj de urgencia y fecha límite."""
    ancho, alto = 1080, 1920
    img = preparar_fondo_con_overlay(TEMPLATES_DIR / "ayuda_autonomo_trabajando.jpg", ancho, alto, oscurecer=130)
    draw = ImageDraw.Draw(img)

    badge_rect = [100, 200, 980, 295]
    draw.rounded_rectangle(badge_rect, radius=24, fill=(234, 179, 8))
    texto_centrado_auto(draw, "⏳ PLAZO DE SOLICITUD ABIERTO", badge_rect, "arialbd.ttf", 38, (15, 23, 42))

    card_rect = [80, 650, 1000, 1080]
    draw.rounded_rectangle(card_rect, radius=32, fill=(15, 23, 42), outline=(220, 38, 38), width=5)

    draw.text((540, 720), "FECHA LÍMITE DE PRESENTACIÓN", font=ImageFont.truetype("arialbd.ttf", 34), fill=(248, 113, 113), anchor="mm")
    draw.text((540, 840), str(ayuda["fecha_fin"]), font=ImageFont.truetype("arialbd.ttf", 75), fill=(255, 255, 255), anchor="mm")

    aviso_rect = [120, 930, 960, 1030]
    draw.rounded_rectangle(aviso_rect, radius=18, fill=(30, 41, 59))
    draw.text((540, 980), "⚠️ Se asigna por orden estricto de entrada", font=ImageFont.truetype("arialbd.ttf", 30), fill=(253, 224, 71), anchor="mm")

    org_rect = [100, 1200, 980, 1310]
    draw.rounded_rectangle(org_rect, radius=20, fill=(30, 41, 59))
    texto_centrado_auto(draw, f"🏛️ Convocado por: {ayuda['organismo']}", org_rect, "arialbd.ttf", 34, (203, 213, 225))

    img.save(ruta_salida, quality=95)

def crear_escena_ayuda_4_cta(ruta_salida: Path):
    """Escena 4: Pantalla de llamada a la acción hacia el canal de Telegram."""
    from src.video_generator.generador_visual_earth import preparar_escena_4_telegram
    preparar_escena_4_telegram(ruta_salida)

async def generar_video_ayuda_visual(ayuda: dict, ruta_video_final: Path):
    """Ensambla el vídeo de alta calidad visual combinando fotos reales y voz neuronal."""
    id_ayuda = ayuda["id_convocatoria"]
    e1 = OUTPUT_DIR / f"ayuda_v_{id_ayuda}_e1.png"
    e2 = OUTPUT_DIR / f"ayuda_v_{id_ayuda}_e2.png"
    e3 = OUTPUT_DIR / f"ayuda_v_{id_ayuda}_e3.png"
    e4 = OUTPUT_DIR / f"ayuda_v_{id_ayuda}_e4.png"

    crear_escena_ayuda_1_notificacion(ayuda, e1)
    crear_escena_ayuda_2_beneficiarios(ayuda, e2)
    crear_escena_ayuda_3_plazo(ayuda, e3)
    crear_escena_ayuda_4_cta(e4)

    ruta_audio = OUTPUT_DIR / f"ayuda_v_{id_ayuda}_audio.mp3"
    ruta_srt = OUTPUT_DIR / f"ayuda_v_{id_ayuda}_sub.srt"
    ruta_ass = OUTPUT_DIR / f"ayuda_v_{id_ayuda}_sub.ass"

    guion_impacto = (
        f"Atentos a esta nueva ayuda oficial que acaba de publicarse. "
        f"Se ha aprobado una dotación directa de {ayuda['presupuesto_formato']} "
        "de dinero a fondo perdido que no tienes que devolver. "
        f"Está destinada a {ayuda['beneficiarios'].lower()[:50]} para impulsar su actividad. "
        f"El plazo ya está abierto y finaliza el {ayuda['fecha_fin']}. "
        "Para ver la convocatoria oficial, los requisitos y el enlace directo a la sede electrónica, "
        "entra en el enlace de nuestro perfil y únete a nuestro canal privado de Telegram. "
        "Tienes el link en la bio."
    )

    com = edge_tts.Communicate(guion_impacto, "es-ES-AlvaroNeural", rate="+6%")
    submaker = edge_tts.SubMaker()
    with open(ruta_audio, "wb") as f_a:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f_a.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
    with open(ruta_srt, "w", encoding="utf-8") as f_s:
        f_s.write(submaker.get_srt())

    convertir_srt_a_ass(ruta_srt, ruta_ass)

    dur_audio = obtener_duracion_audio(ruta_audio)
    dur_e1 = 4.5
    dur_e2 = 5.5
    dur_e3 = 5.5
    dur_e4 = max(7.0, (dur_audio - (dur_e1 + dur_e2 + dur_e3)) + 2.0)
    duraciones = [dur_e1, dur_e2, dur_e3, dur_e4]

    print(f"🎬 Ensamblando vídeo ultra-visual de ayuda ({sum(duraciones):.1f}s)...")
    ensamblar_video_cinematico([e1, e2, e3, e4], duraciones, ruta_audio, ruta_ass, ruta_video_final)
    print(f"🚀 ¡VÍDEO ULTRA-VISUAL GENERADO CON ÉXITO!: {ruta_video_final}")
