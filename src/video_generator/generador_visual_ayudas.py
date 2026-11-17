"""
Generador de Vídeos Verticales para Ayudas y Subvenciones (TikTok / Reels / Shorts)
Reutiliza el motor gráfico y cinemático a coste 0,00 €.
"""
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

from src.video_generator.generador_visual_earth import (
    obtener_ruta_ffmpeg,
    obtener_duracion_audio,
    texto_centrado_auto,
    convertir_srt_a_ass,
    ensamblar_video_cinematico
)

def crear_escena_ayuda_1(ayuda: dict, ruta_salida: Path):
    """Escena 1: El gancho oficial con sello de urgencia."""
    ancho, alto = 1080, 1920
    img = Image.new("RGB", (ancho, alto), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Rejilla decorativa de fondo
    for y in range(0, alto, 120):
        draw.line([(0, y), (ancho, y)], fill=(30, 41, 59), width=1)

    # Badge de cabecera urgente
    b_rect = [100, 200, 980, 310]
    draw.rounded_rectangle(b_rect, radius=24, fill=(234, 179, 8))
    texto_centrado_auto(draw, "💰 AYUDA OFICIAL A FONDO PERDIDO", b_rect, "arialbd.ttf", 40, (15, 23, 42))

    # Tarjeta de Convocatoria
    c_rect = [80, 520, 1000, 950]
    draw.rounded_rectangle(c_rect, radius=32, fill=(30, 41, 59), outline=(234, 179, 8), width=5)
    
    draw.text((540, 600), "CONVOCATORIA PÚBLICA", font=ImageFont.truetype("arialbd.ttf", 36), fill=(148, 163, 184), anchor="mm")
    
    # Título auto-ajustado
    t_rect = [120, 660, 960, 880]
    texto_centrado_auto(draw, ayuda["titulo"].upper()[:85], t_rect, "arialbd.ttf", 46, (255, 255, 255))

    # Badge inferior de organismo
    org_rect = [100, 1080, 980, 1200]
    draw.rounded_rectangle(org_rect, radius=20, fill=(51, 65, 85))
    texto_centrado_auto(draw, f"🏛️ {ayuda['organismo']}", org_rect, "arialbd.ttf", 36, (226, 232, 240))

    img.save(ruta_salida, quality=95)

def crear_escena_ayuda_2(ayuda: dict, ruta_salida: Path):
    """Escena 2: La cuantía económica destacada."""
    ancho, alto = 1080, 1920
    img = Image.new("RGB", (ancho, alto), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    b_rect = [100, 200, 980, 310]
    draw.rounded_rectangle(b_rect, radius=24, fill=(34, 197, 94))
    texto_centrado_auto(draw, "💶 PRESUPUESTO ASIGNADO", b_rect, "arialbd.ttf", 42, (15, 23, 42))

    # Tarjeta con la cifra de dinero gigante
    money_rect = [80, 500, 1000, 900]
    draw.rounded_rectangle(money_rect, radius=32, fill=(20, 83, 45), outline=(34, 197, 94), width=6)
    draw.text((540, 590), "PARTIDA OFICIAL APROBADA", font=ImageFont.truetype("arialbd.ttf", 36), fill=(187, 247, 208), anchor="mm")
    draw.text((540, 730), ayuda["presupuesto_formato"], font=ImageFont.truetype("arialbd.ttf", 100), fill=(255, 255, 255), anchor="mm")

    # Sello de NO HAY QUE DEVOLVERLO
    stamp_rect = [120, 1050, 960, 1180]
    draw.rounded_rectangle(stamp_rect, radius=24, fill=(30, 41, 59), outline=(234, 179, 8), width=3)
    texto_centrado_auto(draw, "✅ ENTREGA DINERARIA SIN DEVOLUCIÓN", stamp_rect, "arialbd.ttf", 36, (253, 224, 71))

    img.save(ruta_salida, quality=95)

def crear_escena_ayuda_3(ayuda: dict, ruta_salida: Path):
    """Escena 3: Quién puede pedirlo y plazo límite."""
    ancho, alto = 1080, 1920
    img = Image.new("RGB", (ancho, alto), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    b_rect = [100, 200, 980, 310]
    draw.rounded_rectangle(b_rect, radius=24, fill=(59, 130, 246))
    texto_centrado_auto(draw, "👥 ¿QUIÉN PUEDE SOLICITARLA?", b_rect, "arialbd.ttf", 40, (255, 255, 255))

    # Tarjeta de beneficiarios
    ben_rect = [80, 480, 1000, 780]
    draw.rounded_rectangle(ben_rect, radius=28, fill=(30, 41, 59), outline=(59, 130, 246), width=4)
    draw.text((540, 550), "PERFIL DEL BENEFICIARIO", font=ImageFont.truetype("arialbd.ttf", 34), fill=(148, 163, 184), anchor="mm")
    texto_centrado_auto(draw, ayuda["beneficiarios"][:70], [100, 600, 980, 740], "arialbd.ttf", 38, (255, 255, 255))

    # Plazo urgente
    p_rect = [80, 880, 1000, 1160]
    draw.rounded_rectangle(p_rect, radius=28, fill=(153, 27, 27), outline=(239, 68, 68), width=4)
    draw.text((540, 960), "⏳ FECHA LÍMITE DE SOLICITUD", font=ImageFont.truetype("arialbd.ttf", 36), fill=(254, 202, 202), anchor="mm")
    draw.text((540, 1070), str(ayuda["fecha_fin"]), font=ImageFont.truetype("arialbd.ttf", 55), fill=(255, 255, 255), anchor="mm")

    img.save(ruta_salida, quality=95)

def crear_escena_ayuda_4_cta(ruta_salida: Path):
    """Escena 4: Pantalla final de llamada a la acción hacia Telegram."""
    from src.video_generator.generador_visual_earth import preparar_escena_4_telegram
    preparar_escena_4_telegram(ruta_salida)

async def generar_video_ayuda(ayuda: dict, ruta_video_final: Path):
    """Genera el vídeo completo sincronizado con voz en off y subtítulos."""
    id_ayuda = ayuda["id_convocatoria"]
    e1 = OUTPUT_DIR / f"ayuda_{id_ayuda}_e1.png"
    e2 = OUTPUT_DIR / f"ayuda_{id_ayuda}_e2.png"
    e3 = OUTPUT_DIR / f"ayuda_{id_ayuda}_e3.png"
    e4 = OUTPUT_DIR / f"ayuda_{id_ayuda}_e4.png"

    crear_escena_ayuda_1(ayuda, e1)
    crear_escena_ayuda_2(ayuda, e2)
    crear_escena_ayuda_3(ayuda, e3)
    crear_escena_ayuda_4_cta(e4)

    ruta_audio = OUTPUT_DIR / f"ayuda_{id_ayuda}_audio.mp3"
    ruta_srt = OUTPUT_DIR / f"ayuda_{id_id}_sub.srt" if False else OUTPUT_DIR / f"ayuda_{id_ayuda}_sub.srt"
    ruta_ass = OUTPUT_DIR / f"ayuda_{id_ayuda}_sub.ass"

    guion = (
        f"Atención a esta nueva ayuda oficial que acaba de publicarse. "
        f"Se ha abierto la convocatoria para {ayuda['titulo'][:60]}. "
        f"Cuenta con una dotación aprobada de {ayuda['presupuesto_formato']} de dinero a fondo perdido "
        "que no tendrás que devolver. "
        f"Está dirigida a {ayuda['beneficiarios'].lower()[:50]} y el plazo de presentación "
        f"está abierto hasta el {ayuda['fecha_fin']}. "
        "Para acceder a la sede electrónica oficial y tramitar la solicitud antes de que se agoten los fondos, "
        "entra en el enlace de nuestro perfil y únete a nuestro canal privado de Telegram. "
        "Tienes el link en la bio."
    )

    # Generar locución
    com = edge_tts.Communicate(guion, "es-ES-AlvaroNeural", rate="+6%")
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
    dur_e1 = 4.0
    dur_e2 = 5.0
    dur_e3 = 5.5
    dur_e4 = max(7.0, (dur_audio - (dur_e1 + dur_e2 + dur_e3)) + 2.0)
    duraciones = [dur_e1, dur_e2, dur_e3, dur_e4]

    print(f"🎬 Ensamblando vídeo de ayuda... Duración total: {sum(duraciones):.1f}s")
    ensamblar_video_cinematico([e1, e2, e3, e4], duraciones, ruta_audio, ruta_ass, ruta_video_final)
    print(f"✅ ¡Vídeo de ayuda completado!: {ruta_video_final}")
